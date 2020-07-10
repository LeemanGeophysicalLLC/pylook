# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Test the `lookfiles` module."""

from pylook.io import (XlookParser)


def test_look_parser_creation():
    """Make sure we can create an empty instance of the look r file parser."""
    XlookParser()
