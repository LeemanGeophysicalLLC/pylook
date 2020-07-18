# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Setup script for pylook."""

import sys

from setuptools import setup

if sys.version_info[0] < 3:
    error = """
    pylook requires Python 3.6 or greater!
    Python {py} detected.
    """.format(py='.'.join([str(v) for v in sys.version_info[:3]]))

    print(error)  # noqa: T001
    sys.exit(1)

setup(use_scm_version={'version_scheme': 'post-release'})
