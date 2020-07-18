.. toctree::
   :maxdepth: 1
   :hidden:

   api/index
   examples/index

======
pylook
======

pylook is a Python library to reduce and process data from rock mechanics laboratory
experiments. It is based upon the xlook tool and replacing it with a modern, sustainable,
and easily installable tool that features a complete test suite and documentation.

pylook is maintained and developed by the open source community. Leeman Geophysical LLC
manages the project.

----------
Contact Us
----------
We're open source! Find a bug? File an issue! `Leeman Geophysical LLC`__ can offer basic support,
but time resources are limited. You can email our `support inbox
<mailto: support@leemangeophysical.com>`_

__ https://www.leemangeophysical.com

--------
Versions
--------
pylook follows `semantic versioning <https://semver.org>`_ in its version number. This means
that any pylook ``1.x`` release will be backwards compatible with an earlier ``1.y`` release.
By "backward compatible", we mean that **correct** code that works on a ``1.y`` version will
work on a future ``1.x`` version. It's always possible for bug fixes to change behavior or make
incorrect code cease to work. Backwards-incompatible changes will only be allowed when changing
to version ``2.0``. Such changes will be proceeded by `pylookDeprecationWarning` or
`FutureWarning` as appropriate. For a version ``1.x.y``, we change ``x`` when we
release new features, and ``y`` when we make a release with only bug fixes.

-------
License
-------

pylook is available under the terms of the open source `BSD 3 Clause license`__.

__ https://raw.githubusercontent.com/leemangeophysicalllc/pylook/master/LICENSE

---------------
Code of Conduct
---------------
We want everyone to feel welcome to contribute to pylook and participate in discussions. In that
spirit please have a look at our `code of conduct`__.

__ https://github.com/leemangeophysicalllc/pylook/blob/master/CODE_OF_CONDUCT.md

------
Thanks
------
This project wouldn't be possible without the support of the countless open-source developers
that donate their time and talents to the Python ecosystem. The structure of pylook is largely
based upon the hard work of Unidata's Python team and their experience with developing and
deploying the MetPy package. Chris Marone funded the initial development of pylook and was
the first to have a vision of auditable and tracked data reduction for the rock mechanics
community when xlook was created.

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
