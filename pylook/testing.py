# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Collection of utilities for testing."""

import numpy as np
import numpy.testing
from pint import DimensionalityError

from .units import units


def check_mask(actual, desired):
    """
    Check that two arrays have the same mask.

    This handles the fact that `~numpy.testing.assert_array_equal` ignores masked values
    in either of the arrays. This ensures that the masks are identical.
    """
    actual_mask = getattr(actual, 'mask', np.full(np.asarray(actual).shape, False))
    desired_mask = getattr(desired, 'mask', np.full(np.asarray(desired).shape, False))
    np.testing.assert_array_equal(actual_mask, desired_mask)


def check_and_drop_units(actual, desired):
    """
    Check that the units on the passed in arrays are compatible; return the magnitudes.

    Parameters
    ----------
    actual : `pint.Quantity` or array-like
    desired : `pint.Quantity` or array-like

    Returns
    -------
    actual, desired
        array-like versions of `actual` and `desired` once they have been
        coerced to compatible units.

    Raises
    ------
    AssertionError
        If the units on the passed in objects are not compatible.
    """
    try:
        # If the desired result has units, add dimensionless units if necessary, then
        # ensure that this is compatible to the desired result.
        if hasattr(desired, 'units'):
            if not hasattr(actual, 'units'):
                actual = units.Quantity(actual, 'dimensionless')
            actual = actual.to(desired.units)
        # Otherwise, the desired result has no units. Convert the actual result to
        # dimensionless units if it is a united quantity.
        else:
            if hasattr(actual, 'units'):
                actual = actual.to('dimensionless')
    except DimensionalityError:
        raise AssertionError('Units are not compatible: {} should be {}'.format(
            actual.units, getattr(desired, 'units', 'dimensionless')))

    if hasattr(actual, 'magnitude'):
        actual = actual.magnitude
    if hasattr(desired, 'magnitude'):
        desired = desired.magnitude

    return actual, desired


def assert_array_almost_equal(actual, desired, decimal=7):
    """
    Check that arrays are almost equal, including units.

    Wrapper around :func:`numpy.testing.assert_array_almost_equal`
    """
    actual, desired = check_and_drop_units(actual, desired)
    check_mask(actual, desired)
    numpy.testing.assert_array_almost_equal(actual, desired, decimal)
