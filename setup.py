# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Setup script for pylook."""

from distutils.core import setup

setup(
    name='pylook',
    version='0.1dev',
    packages=['pylook', ],
    license='MIT',
    long_description=('Provides tools to reduce and analyze data from experimental'
                      ' rock mechanics laboratories.'),
)
