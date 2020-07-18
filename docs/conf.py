# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os

import pylook


# -- Project information -----------------------------------------------------

project = 'pylook'
copyright = '2020, Leeman Geophysical LLC'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_gallery.gen_gallery',
    'sphinx.ext.napoleon'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
try:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
except ImportError:
    pass

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = ['theme_override.css']

# Controlling automatically generating summary tables in the docs
autosummary_generate = True
autosummary_imported_members = True

# Control main class documentation
autoclass_content = 'both'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
verinfo = pylook.__version__
full_version = verinfo.split('+')[0]
version = full_version.rsplit('.', 1)[0]
# The full version, including alpha/beta/rc tags.
release = verinfo

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

sphinx_gallery_conf = {
    'doc_module': ('pylook',),
    'reference_url': {
        'pylook': None,
    },
    'examples_dirs': [os.path.join('..', 'examples')],
    'gallery_dirs': ['examples'],
    'filename_pattern': r'\.py',
    'backreferences_dir': os.path.join('api', 'generated'),
    #'default_thumb_file': os.path.join('_static', 'pylook_150x150_white_bg.png'),
    'abort_on_example_error': True
}

# Tweak how docs are formatted
napoleon_use_rtype = False

