# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Contains utilities to work with "look" style data files."""

import struct
import warnings

import numpy as np
from pint.errors import UndefinedUnitError

from pylook.units import units
from ..package_tools import Exporter

exporter = Exporter(globals())


def _binary_tuple_to_string(binary_form):
    binary_form = [c.decode() for c in binary_form]
    return ''.join(binary_form)


@exporter.export
def read_binary(filename, data_endianness='little', unrecognized_units='ignore',
                clean_header=True):
    """
    Read a look binary formatted file into a dictionary of united arrays.

    Parameters
    ----------
    filename : string
        Filename or path to file to read
    data_endianness: string
        Endianness of the data section of the file. 'big' or 'little' (default).
    unrecogized_units : string
        'ignore' (defualt) assigns dimensionless to unrecognized units, 'error' will
        fail if unrecognized units are encountered.
    clean_header : boolean
        Remove extra whitespace in the header data column names and units. Default True.

    Returns
    -------
    data : dict
        Dictionary of `pint.Quantity` arrays for each column of data.
    metadata : dict
        Metadata from the header of the file

    Notes
    -----
    The data section of the file is written in the native format of the machine
    used to produce the file.  Endianness of data is little by default, but may
    be changed to 'big' to accomodate older files or files written on power pc
    chips.
    """
    with open(filename, 'rb') as f:

        col_headings = []
        col_recs = []
        col_units = []
        metadata = {}

        # Unpack information at the top of the file about the experiment
        name = struct.unpack('20c', f.read(20))
        name = _binary_tuple_to_string(name)
        name = name.split('\0')[0]
        if clean_header:
            name = name.strip()
            metadata['name'] = name
        # The rest of the header information is written in big endian format

        # Number of records (int)
        num_recs = struct.unpack('>i', f.read(4))
        num_recs = int(num_recs[0])
        metadata['number of records'] = num_recs

        # Number of columns (int)
        num_cols = struct.unpack('>i', f.read(4))
        num_cols = int(num_cols[0])
        metadata['number of columns'] = num_cols

        # Sweep (int) - No longer used
        swp = struct.unpack('>i', f.read(4))[0]
        metadata['swp'] = swp

        # Date/time(int) - No longer used
        dtime = struct.unpack('>i', f.read(4))[0]
        metadata['dtime'] = dtime

        # For each possible column (32 maximum columns) unpack its header
        # information and store it.  Only store column headers of columns
        # that contain data.  Use termination at first NULL.
        for i in range(32):

            # Channel name (13 characters)
            chname = struct.unpack('13c', f.read(13))
            chname = _binary_tuple_to_string(chname)
            chname = chname.split('\0')[0]

            # Channel units (13 characters)
            chunits = struct.unpack('13c', f.read(13))
            chunits = _binary_tuple_to_string(chunits)
            chunits = chunits.split('\0')[0]

            # This field is now unused, so we just read past it (int)
            _ = struct.unpack('>i', f.read(4))

            # This field is now unused, so we just read past it (50 characters)
            comment = struct.unpack('50c', f.read(50))
            comment = _binary_tuple_to_string(comment)

            # Number of elements (int)
            nelem = struct.unpack('>i', f.read(4))
            nelem = int(nelem[0])

            if clean_header:
                chname = chname.strip()
                chunits = chunits.strip()
                comment = comment.strip()

            if chname[0:6] == 'no_val':
                continue  # Skip Blank Channels
            else:
                col_headings.append(chname)
                col_recs.append(nelem)
                col_units.append(chunits)

        # Read the data into a numpy recarray
        data = np.empty([num_recs, num_cols])

        for col in range(num_cols):
            for row in range(col_recs[col]):
                if data_endianness == 'little':
                    data[row, col] = struct.unpack('<d', f.read(8))[0]
                elif data_endianness == 'big':
                    data[row, col] = struct.unpack('>d', f.read(8))[0]
                else:
                    ValueError('Data endian setting invalid - options are little and big')

    data_dict = {}
    for i, (name, unit) in enumerate(zip(col_headings, col_units)):
        data_unit = units('dimensionless')
        try:
            data_unit = units(unit)

        except UndefinedUnitError:
            if unrecognized_units == 'ignore':
                warnings.warn(f'Unknown unit {unit} - assigning dimensionless units.')
            else:
                raise UndefinedUnitError(unit)

        data_dict[name] = data[:, i] * data_unit

    return data_dict, metadata
