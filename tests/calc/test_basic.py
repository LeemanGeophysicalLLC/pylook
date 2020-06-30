# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Test the `basic` module."""

import numpy as np

from pylook.calc import (remove_offset, zero)
from pylook.testing import assert_array_almost_equal
from pylook.units import units


def test_zero_defaults():
    """Test zero with all of the default args."""
    data = np.arange(10) * units('mm')

    result = zero(data, 5)

    truth = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]) * units('mm')

    assert_array_almost_equal(result, truth)


def test_zero_mode_before():
    """Test zero with the mode of before."""
    data = np.arange(10) * units('mm')

    result = zero(data, 5, mode='before')

    truth = np.array([0, 0, 0, 0, 0, 0, 1, 2, 3, 4]) * units('mm')

    assert_array_almost_equal(result, truth)


def test_zero_mode_after():
    """Test zero with the mode of after."""
    data = np.arange(10) * units('mm')

    result = zero(data, 5, mode='after')

    truth = np.array([-5, -4, -3, -2, -1, 0, 0, 0, 0, 0]) * units('mm')

    assert_array_almost_equal(result, truth)


def test_zero_window():
    """Test zero with a window to get an average zero value."""
    data = np.array([0, 1, 2, 2.2, 2.5, 2.3, 2.2, 2.6, 2.7, 2.9, 3]) * units('mm')

    result = zero(data, 5, window=2)

    truth = data - 2.36 * units('mm')

    assert_array_almost_equal(result, truth)


def test_zero_value_at_mode():
    """Test zeroing with an offset value in the default at mode."""
    data = np.arange(10) * units('mm')

    result = zero(data, 5, value=1.5 * units('mm'))

    truth = np.array([-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]) * units('mm')

    assert_array_almost_equal(result, truth)


def test_zero_value_before_mode():
    """Test zeroing with an offset value in the before mode."""
    data = np.arange(10) * units('mm')

    result = zero(data, 5, value=1.5 * units('mm'), mode='before')

    truth = np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.5, 3.5, 4.5, 5.5]) * units('mm')

    assert_array_almost_equal(result, truth)


def test_zero_value_after_mode():
    """Test zeroing with an offset value in the after mode."""
    data = np.arange(10) * units('mm')

    result = zero(data, 5, value=1.5 * units('mm'), mode='after')

    truth = np.array([-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 1.5, 1.5, 1.5, 1.5]) * units('mm')

    assert_array_almost_equal(result, truth)


def test_remove_offset():
    """Test the remove offset function."""
    data = np.array([0, 1, 2, 4, 4, 10, 10, 11, 12, 13, 14]) * units('mm')

    result = remove_offset(data, 4, 6)

    truth = np.array([0, 1, 2, 4, 4, 4, 4, 5, 6, 7, 8]) * units('mm')

    assert_array_almost_equal(result, truth)
