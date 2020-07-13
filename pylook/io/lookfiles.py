# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""Contains utilities to work with "look" style data files and associated "r" files."""

from pathlib import Path
import struct
import warnings

import numpy as np
from pint.errors import UndefinedUnitError

import pylook.calc as lc
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
    data_dict['rec_num'] = np.arange(num_recs) * units('dimensionless')

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


@exporter.export
class XlookParser:
    """Xlook R File Parser."""

    def __init__(self):
        """Initialize the parser with 32 empty columns to match the Look data model."""
        self.max_cols = 32
        self.data = [np.array([]) for i in range(self.max_cols)]
        self.data_units = [None for i in range(self.max_cols)]
        self.data_names = [None for i in range(self.max_cols)]

    def _get_data_by_index(self, index):
        """
        Get a data array by its zero based index column number.

        Parameters
        ----------
        index : int
            Index (zero based) of the data column to get.

        Returns
        -------
        data : `pint.Quantity`
            Data array.
        """
        return self.data[index]

    def _get_units_by_index(self, index):
        """
        Get the units associated with the zero based column number.

        Parameters
        ----------
        index : int
            Index (zero based) of the data column unit to get

        Returns
        -------
        unit : str
            String representation of the column units
        """
        return self.data_units[index]

    def _get_name_by_index(self, index):
        """
        Get the name for a column associated with the zero based column number.

        Parameters
        ----------
        index : int
            Index (zero based) of the data column name to get

        Returns
        -------
        name : str
            Name of the data column
        """
        return self.data_names[index]

    def _set_units_by_index(self, index, units):
        """
        Store the units associated with a column based on its zero based column number.

        Parameters
        ----------
        index : int
            Index (zero based) of the data column unit to set
        units : str
            Unit name to associate with the data column
        """
        self.data_units[index] = units

    def _set_name_by_index(self, index, name):
        """
        Set the name associated with a column based on its zero based column number.

        Parameters
        ----------
        index : int
            Index (zero based) of the data column name to set
        name : str
            Name to associate with the data column
        """
        self.data_names[index] = name

    def _set_data_by_index(self, index, data):
        """
        Store data into a given zero based index position.

        Parameters
        ----------
        index : int
            Index (zero based) of the data column to set
        data : `pint.Quantity`
            Data to associate with the data column
        """
        self.data[index] = data

    def doit(self, rfile):
        """
        Run an r-file - naming directly from XLook itself for ease of learning for new users.

        Parameters
        ----------
        rfile : str
            Path to r file to run
        """
        with open(rfile, 'r') as f:
            for line in f.readlines():
                # If there is an in-line comment, we split and just keep the first part
                if '#' in line:
                    line = line.split('#')[0].strip()

                # If it is an end command - bounce out of doit
                if line.strip() == 'end':
                    return
                self.parse_line(line)

    def parse_line(self, line):
        """
        Parse the text in an xlook command and execute the appropriate function.

        Parameters
        ----------
        line : str
            Xlook command line to process
        """
        # Kill any trailing whitespaces
        line = line.strip()

        # There doesn't have to be a space after the #, so let's just short circuit
        # here for any line starting with a #.
        if (line.startswith('#')) or (line.strip() == ''):
            self.command_comment(line)
            return

        # Split up the command into the root and the rest
        command_root = line.strip().split(' ')[0]

        # There were never supposed to be commas in the lines, but some files
        # had them - XLook just ignored them so we do the same
        line = line.replace(',', '')

        # Dictionary mapping commands to their functions
        command_functions = {'math': self.command_math,
                             'begin': self.command_begin,
                             'com_file': self.command_com_file,
                             'summation': self.command_summation,
                             'power': self.command_power,
                             'zero': self.command_zero,
                             'ec': self.command_ec,
                             'r_col': self.command_r_col,
                             'math_int': self.command_math_int,
                             'offset_int': self.command_offset_int,
                             'r_row': self.command_r_row,
                             #  'type': self.command_type,
                             'read': self.command_read}

        # Determine the function that we should run - if there isn't a matching function
        # we issue a warning and keep running. That's what xLook did.
        action_function = command_functions.get(command_root)
        if action_function is None:
            action_function = self.command_invalid

        action_function(line.strip())

    def command_math(self, command):
        r"""
        Perform math operations with columns of data.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The XLook command is `math x_col_number operator y_col_number type new_col_number`
        where the operator can be \*, /, +, or -. Type indicates if the operation is between
        two columns (element-wise calculation) if : or if the operation is between a column
        and a scalar if =.
        """
        if not self._check_number_of_arguments(command, 8):
            return

        (_, arg_1, operation, arg_2, type_of_math,
         output_col_idx, output_name, output_unit) = command.split(' ')

        arg_1 = int(arg_1)
        output_col_idx = int(output_col_idx)
        output_name = output_name.strip()
        output_unit = output_unit.strip()

        # The first arg is always a column, we get that data
        first_arg_data = self._get_data_by_index(arg_1)

        # Determine the second operand - column or scalar
        # If the type of math is : then it's an element by element operation between columns
        # If the type of math is = then it's a column and scalar operation
        if type_of_math == ':':
            arg_2 = int(arg_2)
            second_arg_data = self._get_data_by_index(arg_2)
        elif type_of_math == '=':
            arg_2 = float(arg_2)
            second_arg_data = arg_2
        else:
            self.command_invalid(command)

        # Determine the operation and do it
        if operation == '*':
            result = first_arg_data * second_arg_data
        elif operation == '/':
            result = first_arg_data / second_arg_data
        elif operation == '+':
            result = first_arg_data + second_arg_data
        elif operation == '-':
            result = first_arg_data - second_arg_data
        else:
            self.command_invalid(command)

        # Put the result back into the output
        self._set_data_by_index(output_col_idx, result)
        self._set_name_by_index(output_col_idx, output_name)
        self._set_units_by_index(output_col_idx, output_unit)

    def command_comment(self, command):
        """
        Process a comment line.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        In XLook, comments are simply ignored, but this function is provided should we find
        the need to log, or otherwise process them (potentially even for metadata extraction).
        """
        pass

    def command_begin(self, command):
        """
        Process the begin command.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The begin command, while essential in XLook is simply ignored here. It denoted the
        start of the file.
        """
        pass

    def command_com_file(self, command):
        """
        Process the com_file command.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The command com_file is ignored here, but indicated that this was a command file
        to XLook.
        """
        pass

    def command_invalid(self, command):
        """
        Process an invalid command.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        Issue a warning for invalid commands, but we keep going just like XLook did. Xlook
        printed a console message, but they were mostly ignored by users, the warning should
        at least grab attention.
        """
        warnings.warn(f'Invalid Command {command} - ignored and processing proceeding.')

    def _check_number_of_arguments(self, command, n_args):
        """
        Check that the command has the required number of arguments.

        Check that we have enough arguments (the command counts as one as well)
        and issue a warning if not.

        Parameters
        ----------
        command : str
            command from r file
        n_args : int
            number of arguments expected with the command (the command counts as one)

        Returns
        -------
        valid : boolean
            If the command has the correct number of arguments.

        Notes
        -----
        Returns False so we can bail on processing that command and keep running like
        XLook did.
        """
        n_args_received = len(command.split(' '))
        if n_args_received != n_args:
            warnings.warn(f'Command {command} expected {n_args}, but received'
                          f' {n_args_received} - ignored and processing proceeding.')
            return False
        return True

    def command_summation(self, command):
        """
        Compute the cumulative sum of a column.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The XLook command is `summation column_number new_column_number`
        """
        if not self._check_number_of_arguments(command, 5):
            return
        (_, input_col_idx, output_col_idx, output_name, output_unit) = command.split(' ')
        input_col_idx = int(input_col_idx)
        output_col_idx = int(output_col_idx)
        result = np.cumsum(self._get_data_by_index(input_col_idx))

        # Put the result back into the output
        self._set_data_by_index(output_col_idx, result)
        self._set_name_by_index(output_col_idx, output_name)
        self._set_units_by_index(output_col_idx, output_unit)

    def command_power(self, command):
        """
        Compute a column raised to a power.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The Xlook command is `power power_value column_number new_column_number`
        """
        if not self._check_number_of_arguments(command, 6):
            return
        (_, power, input_col_idx, output_col_idx,
         output_name, output_unit) = command.split(' ')
        input_col_idx = int(input_col_idx)
        output_col_idx = int(output_col_idx)
        power = float(power)
        result = self._get_data_by_index(input_col_idx) ** power

        # Put the result back into the output
        self._set_data_by_index(output_col_idx, result)
        self._set_name_by_index(output_col_idx, output_name)
        self._set_units_by_index(output_col_idx, output_unit)

    def command_zero(self, command):
        """
        Zero a column at a record.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The Xlook command is `zero column_number record_index`.

        See Also
        --------
        pylook.calc.zero
        """
        if not self._check_number_of_arguments(command, 3):
            return
        (_, input_col_idx, zero_record) = command.split(' ')
        input_col_idx = int(input_col_idx)
        zero_record = int(zero_record)
        result = lc.zero(self._get_data_by_index(input_col_idx) * units('dimensionless'),
                         zero_record)
        self._set_data_by_index(input_col_idx, result.m)  # We are not touching units and names

    def command_ec(self, command):
        """
        Perform a linear elastic correction of a column.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        This is not unit safe like the pure Python version would be as we're shedding units
        all around in the interpreter. The XLook command was `ec displacement_column_number
        load_column_number new_column_number first_row_index last_row_index`
        """
        if not self._check_number_of_arguments(command, 9):
            return

        (_, disp_col_idx, load_col_idx, output_col_idx,
         first_idx, last_idx, slope, output_name, output_unit) = command.split(' ')
        disp_col_idx = int(disp_col_idx)
        load_col_idx = int(load_col_idx)
        output_col_idx = int(output_col_idx)
        first_idx = int(first_idx)
        last_idx = int(last_idx)
        slope = 1 / float(slope)

        # Get the data and assign units - they don't matter we just need them for the
        # pylook functions to work
        load_data = self._get_data_by_index(load_col_idx) * units('dimensionless')
        disp_data = self._get_data_by_index(disp_col_idx) * units('dimensionless')
        coeffs = [slope * units('dimensionless'), 0 * units('dimensionless')]

        ec_corrected_disp = disp_data - lc.elastic_correction(load_data, disp_data, coeffs)

        # Drop our unit charade
        ec_corrected_disp = ec_corrected_disp.m
        disp_data = disp_data.m

        disp_data[first_idx: last_idx] = ec_corrected_disp[first_idx: last_idx]
        self._set_data_by_index(output_col_idx, disp_data)
        self._set_name_by_index(output_col_idx, output_name)
        self._set_units_by_index(output_col_idx, output_unit)

    def command_r_col(self, command):
        """
        Remove a given column by setting it to empty and the name/units to None.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The Xlook command is `r_col column_number`
        """
        if not self._check_number_of_arguments(command, 2):
            return
        _, col_idx = command.split(' ')
        col_idx = int(col_idx)
        # Set to empty and None for names and units
        self._set_data_by_index(col_idx, np.empty_like(self._get_data_by_index(col_idx)))
        self._set_name_by_index(col_idx, None)
        self._set_units_by_index(col_idx, None)

    def command_math_int(self, command):
        """
        Perform a math operation on an interval of a column.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The Xlook command is math_int x_col_number operator y_col_number type new_col_number
        first_row_index last_row_index`
        """
        if not self._check_number_of_arguments(command, 10):
            return

        (_, arg_1, operation, arg_2, type_of_math,
         output_col_idx, start_idx, stop_idx, output_name, output_unit) = command.split(' ')

        arg_1 = int(arg_1)
        output_col_idx = int(output_col_idx)
        start_idx = int(start_idx)
        stop_idx = int(stop_idx)
        output_name = output_name.strip()
        output_unit = output_unit.strip()

        # The first arg is always a column, we get that data
        first_arg_data = self._get_data_by_index(arg_1)

        # Determine the second operand - column or scalar
        # If the type of math is : then it's an element by element operation between columns
        # If the type of math is = then it's a column and scalar operation
        if type_of_math == ':':
            arg_2 = int(arg_2)
            second_arg_data = self._get_data_by_index(arg_2)
        elif type_of_math == '=':
            arg_2 = float(arg_2)
            second_arg_data = arg_2
        else:
            self.command_invalid(command)

        # Determine the operation and do it
        if operation == '*':
            result = first_arg_data * second_arg_data
        elif operation == '/':
            result = first_arg_data / second_arg_data
        elif operation == '+':
            result = first_arg_data + second_arg_data
        elif operation == '-':
            result = first_arg_data - second_arg_data
        else:
            self.command_invalid(command)

        first_arg_data[start_idx: stop_idx] = result[start_idx: stop_idx]

        # Put the result back into the output
        self._set_data_by_index(output_col_idx, first_arg_data)
        self._set_name_by_index(output_col_idx, output_name)
        self._set_units_by_index(output_col_idx, output_unit)

    def command_offset_int(self, command):
        """
        Perform an offset over an interval in the data.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The Xlook command is `offset_int column_number record_start_index record_end_index
        (y or n) to offset in between during the offset.`
        """
        if not self._check_number_of_arguments(command, 5):
            return

        (_, col_idx, start_idx, stop_idx, set_between) = command.split(' ')
        col_idx = int(col_idx)
        start_idx = int(start_idx)
        stop_idx = int(stop_idx)
        if set_between.strip().lower() == 'y':
            set_between = True
        elif set_between.strip().lower() == 'n':
            set_between = False
        else:
            self.command_invalid()

        col_data = self._get_data_by_index(col_idx)

        col_data = lc.remove_offset(col_data * units('dimensionless'), start_idx, stop_idx,
                                    set_between=set_between)

        self._set_data_by_index(col_idx, col_data.m)

    def command_r_row(self, command):
        """
        Remove a range of rows from all columns of data.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The Xlook command is `r_row column_number first_row_index last_row_index`.
        """
        if not self._check_number_of_arguments(command, 3):
            return
        _, start_row_idx, end_row_idx = command.split(' ')
        start_row_idx = int(start_row_idx)
        end_row_idx = int(end_row_idx)
        if end_row_idx == -1:
            end_row_idx = None
        slice_to_delete = slice(start_row_idx, end_row_idx, None)
        for col_idx in range(self.max_cols):
            self._set_data_by_index(col_idx, np.delete(self._get_data_by_index(col_idx),
                                                       slice_to_delete))

    def command_read(self, command):
        """
        Read a binary file in for processing.

        Parameters
        ----------
        command : str
            command from r file

        Notes
        -----
        The Xlook command is `read filename`
        """
        if not self._check_number_of_arguments(command, 2):
            return
        _, fpath = command.split(' ')
        fpath = Path(fpath.strip())

        data_dict, _ = read_binary(fpath)

        # Break the data dict out into the structure of the class
        for i, (name, data_col) in enumerate(data_dict.items()):
            self._set_data_by_index(i, data_col.m)
            self._set_name_by_index(i, name)
            self._set_units_by_index(i, str(data_col.units))
