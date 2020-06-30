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
