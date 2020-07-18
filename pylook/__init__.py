# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Tools to process and reduce experimental rock mechanics data."""

import sys

if sys.version_info < (3,):
    raise ImportError(
        """
        You are running Python 2 which is a no longer supported version of Python and not
        compatible with pylook.
        """)

from ._version import get_version  # noqa: E402
__version__ = get_version()
del get_version
