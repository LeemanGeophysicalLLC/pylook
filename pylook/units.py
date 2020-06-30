# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""
Module to provide unit support.

This makes use of the :mod:`pint` library and sets up the default settings
for good temperature support.

Attributes
----------
units : :class:`pint.UnitRegistry`
    The unit registry used throughout the package. Any use of units in MetPy should
    import this registry and use it to grab units.
"""
import functools
import logging
import re
import warnings

import pint
import pint.unit

log = logging.getLogger(__name__)

UndefinedUnitError = pint.UndefinedUnitError
DimensionalityError = pint.DimensionalityError

# Create registry, with preprocessors for UDUNITS-style powers (m2 s-2) and percent signs
units = pint.UnitRegistry(
    autoconvert_offset_to_baseunit=True,
    preprocessors=[
        functools.partial(
            re.sub,
            r'(?<=[A-Za-z])(?![A-Za-z])(?<![0-9\-][eE])(?<![0-9\-])(?=[0-9\-])',
            '**'
        ),
        lambda string: string.replace('%', 'percent')
    ]
)

# Capture v0.10 NEP 18 warning on first creation
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    units.Quantity([])

# For pint 0.6, this is the best way to define a dimensionless unit. See pint #185
units.define(pint.unit.UnitDefinition('percent', '%', (),
             pint.converters.ScaleConverter(0.01)))

# Silence UnitStrippedWarning
if hasattr(pint, 'UnitStrippedWarning'):
    warnings.simplefilter('ignore', category=pint.UnitStrippedWarning)

# Enable pint's built-in matplotlib support
units.setup_matplotlib()

del pint
