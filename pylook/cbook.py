# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""Collection of generally useful utility code from the cookbook."""

import os

import pooch

from . import __version__

POOCH = pooch.create(
    path=pooch.os_cache('pylook'),
    base_url='https://github.com/leemangeophysicalllc/pylook/raw/{version}/staticdata/',
    version='v' + __version__,
    version_dev='master')

# Check if we have the data available directly from a git checkout, either from the
# TEST_DATA_DIR variable, or looking relative to the path of this module's file. Use this
# to override Pooch's path.
dev_data_path = os.environ.get('TEST_DATA_DIR',
                               os.path.join(os.path.dirname(__file__),
                                            '..', 'staticdata'))

if os.path.exists(dev_data_path):
    POOCH.path = dev_data_path

POOCH.load_registry(os.path.join(os.path.dirname(__file__), 'static-data-manifest.txt'))


def get_test_data(fname, as_file_obj=False, mode='rb'):
    """
    Access a file from the collection of test data.

    Parameters
    ----------
    fname : str
        Name of test data file to get
    as_file_obj : boolean
        If the file path should be returned (False, default) or a file like object should be
        opened and returned (True).
    mode : str
        Mode in which to open the file like object.
    """
    path = POOCH.fetch(fname)
    # If we want a file object, open it, trying to guess whether this should be binary mode
    # or not
    if as_file_obj:
        return open(path, mode)

    return path
