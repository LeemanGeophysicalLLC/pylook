# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Test the `basic` module."""

import numpy as np

from pylook.calc import (elastic_correction, remove_offset, zero)
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


def test_elastic_correction_linear_same_units():
    """Test the elastic correction with all consistent units given."""
    coeffs = [5 * units('mm/kN'), 10 * units('mm')]
    loads = np.arange(10, 101, 10) * units('kN')
    displacements = (np.arange(1, 11) * 1000) * units('mm')

    result = elastic_correction(loads, displacements, coeffs)

    truth = np.array([940, 1890, 2840, 3790, 4740, 5690, 6640, 7590, 8540, 9490]) * units('mm')
    assert_array_almost_equal(result, truth)


def test_elastic_correction_linear_different_units():
    """Test the elastic correction with inconsistent units given."""
    coeffs = [5 * units('mm/kN'), 10 * units('mm')]
    loads = (np.arange(10, 101, 10) * 1000) * units('N')
    displacements = (np.arange(1, 11) * 1000000) * units('micron')

    result = elastic_correction(loads, displacements, coeffs)

    truth = np.array([940000, 1890000, 2840000, 3790000, 4740000,
                      5690000, 6640000, 7590000, 8540000, 9490000]) * units('micron')
    assert_array_almost_equal(result, truth)


def test_elastic_correction_quadratic_same_units():
    """Test the elastic correction with all consistent units given."""
    coeffs = [2 * units('mm/kN**2'), 5 * units('mm/kN'), 10 * units('mm')]
    loads = np.arange(10, 101, 10) * units('kN')
    displacements = (np.arange(1, 11) * 1000) * units('mm')

    result = elastic_correction(loads, displacements, coeffs)

    truth = np.array([740, 1090, 1040, 590, -260, -1510, -3160, -5210,
                      -7660, -10510]) * units('mm')
    assert_array_almost_equal(result, truth)
