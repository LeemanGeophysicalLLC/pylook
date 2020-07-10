# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Contains basic calculations needed when processing data."""

import numpy as np

from ..package_tools import Exporter

exporter = Exporter(globals())


@exporter.export
def zero(data, zero_idx, window=0, value=0, mode='at'):
    """
    Zero an array at a given row to zero or another value.

    Parameters
    ----------
    data : `pint.Quantity`
        Data to be operated upon.
    zero_idx : int
        Index of value at which we wish to zero the array
    window : int
        Number of data points either side of the zero index to be averaged to get the
        zero value.
    value : `pint.Quantity`
        Numeric value to which we set the "zero" point.
    mode : string
        How the zero operation should be performed. Valid modes at "at" in which only the
        zero value is subtracted from all data, "before" in which all data before that index
        are also set to the zero value, or "after" in which all data after the given index
        are also set to the zero value.

    Returns
    -------
    data : `pint.Quantity`
        Data with zero applied.
    """
    # First we get the value we are going to use as zero - a single value or a mean
    if window:
        zero_value = np.mean(data[zero_idx - window: zero_idx + window + 1])
    else:
        zero_value = data[zero_idx]

    # Zero the data to that value
    data = data - zero_value

    # If there is a value we want to set the data to, add it
    if value:
        data = data + value

    # If the mode is before/after we need to zero out those values
    if mode == 'before':
        data[0:zero_idx] = data[zero_idx]

    if mode == 'after':
        data[zero_idx:] = data[zero_idx]

    return data


@exporter.export
def remove_offset(data, start_idx, end_idx, set_between=False):
    """
    Remove offsets in the data.

    Parameters
    ----------
    data : `pint.Quantity`
        Date to be operated upon.
    start_idx : int
        Index that marks the start of the offset.
    end_idx : int
        Index that marks the end of the offset.
    set_between : int
        Set the data after the start point up to the end point to have the
        value of the start point. Default is `False`.

    Returns
    -------
    data : `pint.Quantity`
        Data with offset applied.
    """
    # Set the data after the offset to the data minus the offset
    offset = data[end_idx] - data[start_idx]

    # Set the intemediate data (during the offset) to be the first
    # value if so desired.
    if set_between:
        data[start_idx: end_idx] = data[start_idx]

    data[end_idx:] = data[end_idx:] - offset
    return data


@exporter.export
def elastic_correction(load, displacement, coeffs):
    """
    Perform an elastic correction on a single axis of data.

    Parameters
    ----------
    load : `pint.Quantity`
        Load/Force data
    displacement : `pint.Quantity`
        Displacement data
    coeffs : list
        list of coefficients from highest power to lowest.

    Returns
    -------
    displacement : `pint.Quantity`
        Displacement with the elastic correction applied
    """
    # store in incoming displacement unit
    displacement_units_incoming = displacement.units

    # convert everythign to base units, then drop them
    load = load.to_base_units().m
    displacement = displacement.to_base_units()
    displacement_base_units = displacement.units
    displacement = displacement.m
    coeffs = [c.to_base_units().m for c in coeffs]

    # Find the elastic correction
    elastic_correction = np.polyval(coeffs, load)

    # Determine the final elastic corrected displacement and attach the base units
    elastic_corrected_displacement = ((displacement - elastic_correction)
                                      * displacement_base_units)

    return elastic_corrected_displacement.to(displacement_units_incoming)


@exporter.export
def friction(shear_component, normal_component):
    """
    Calculate the simple friction.

    Parameters
    ----------
    shear_component : `pint.Quantity`
        Shear component of load/force/stress
    normal_component : `pint.Quantity`
        Normal component of load/force/stress

    Returns
    -------
    friction : `pint.Quantity`
        Simple friction value

    Notes
    -----
    Modifies the normal load/force/ stress to have a minimum value of 1e-16 to avoid any divide
    by zero warnings or negative friction values due to the normal component.
    """
    # Clip the normal component to always be slightly above zero
    normal_component = np.clip(normal_component, 1e-16 * normal_component.units, None)
    return shear_component / normal_component
