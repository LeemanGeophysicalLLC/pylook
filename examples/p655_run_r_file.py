# Copyright (c) 2020 Leeman Geophysical LLC.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

"""
===============================
Running the P655 Reduction File
===============================

Experiment p655 was run in 2005 by Mckiernan, Rathbun, and Rowe. It was reduced by Chris
Marone. Here we use the xlook r file parser to run that r file and then get it into the
dictionary of quantity arrays like we use everywhere else and do some simple plotting of the
experiment.

For the curious, this experiment is determining the frictional response of "Ghost Rocks"
from Kodiak Alaska.

First we import a few things so we can get at the test data and we import the xlook parser
object.
"""
##############################
from pylook.cbook import get_test_data
from pylook.io import XlookParser

##############################
# We use pooch to get test data when you run this notebook for the first time, so you won't
# have to use that `get_test_data` function - it's a helper we use to make running pylook
# examples easy! We run it on the r file and the data file so we're sure that both are
# downloaded to your system. In your world, you'll just need to set the `r_file_path` variable
# to the path to your r file. We recommend using pathlib to do this so your code is portable
# across operating systems!

r_file_path = get_test_data('p655_r')

# Getting the l file as well, just so we're sure it's downloaded!
_ = get_test_data('p655intact100l')

##############################
# We need to create an instance of the parser - this is an object that stores all of the
# commands and parsing instructions for interpreting r files and running them.

look = XlookParser()

##############################
# As a hat tip to xlook, we call the `doit` method on our parser to run the r file.
look.doit(r_file_path)

##############################
# Just as xlook did, unknown commands are ignored. In this case we see warnings that the
# strain command is unknown (i.e. we haven't implemented it yet) and there are some follow on
# consequences from that calculation not happening, but we keep running and get valid output!

# The data are currently in a list of arrays in the object, but we want to get the same data
# structure we work with when dealing with data in pure Python - a dictionary of quantity
# arrays! That can be tricky because we need to assign units which are sometimes misspelled
# or just odd. The `get_data_dict` method will do its best, but ultimately fail with unknown
# units. With the `ignore_unknown_units` argument set to `True` it will warn and assign
# dimensionless to anything it doesn't understand. You can also manually specify units for
# all columns, but it is generally easier to fix it up later in practice.

d = look.get_data_dict(ignore_unknown_units=True)

##############################
# Import our unit registry and fix up the bad units to microns as they should have been.
from pylook.units import units

# Fix up that bad unit name
d['ec_disp'] = d['ec_disp'] * units('micron')

##############################
# We'll use Bokeh to take a quick look at the data. Matplotlib is the best choice for your
# publication plots, but the speed and interactivity of Bokeh in the notebook is hard to beat.
# We'll be adding helpers to pylook to make this process easier in the future as well.

# We need to do some imports from bokeh and turn on the notebook backend.

from bokeh.io import output_notebook
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show

output_notebook()

##############################
# This is a handy function that will be integrated into pylook in a more advanced way soon,
# but demonstrates how to make a flexible plotting function instead of copying and pasting a
# bunch of code over and over again.


def make_runplot(data, x_var='Time', y_vars=None,
                 tools='pan,wheel_zoom,box_zoom,reset,save,box_select,hover'):
    plots = []
    for col_name in list(data):
        if col_name == x_var:
            continue
        if y_vars and (col_name not in y_vars):
            continue

        # First plot is simple, the rest we share the x range with the first
        if plots == []:
            p = figure(title=col_name, tools=tools)
        else:
            p = figure(title=col_name, tools=tools, x_range=plots[0].x_range)

        # Plot the data and set the labels
        p.xaxis.axis_label = str(data[x_var].units)
        p.yaxis.axis_label = str(data[col_name].units)
        p.line(data[x_var].m, data[col_name].m)

        plots.append(p)
    show(gridplot(plots, ncols=1, plot_width=600, plot_height=175))

##############################
# By default make_runplot would plot all of the variables, let's just plot a couple of basic
# ones. Hover over the graph to see the values! That can be turned off by clicking the message
# bubble icon in the plot toolbar. If we don't specify, data are plotted with respect to time.


make_runplot(d, y_vars=['Shear_stress', 'Nor_stress'])


##############################
# We can specify to plot relative to another x variable though - with load point displacement
# probably being the most common.

make_runplot(d, x_var='LP_disp', y_vars=['Shear_stress', 'Nor_stress'])

##############################
# That's it! Running the r file for an experiment created for xlook is really just a few lines
# and then we can pull it into the pylook framework easily to manipualte that data with all of
# Python's power. For new experiments, we recommend reducing the experiment in pure Python
# (see other examples), but being able to read and look at older experiments with no fiddling
# is important to utilize the massive amounts of data already collected and reduced.
