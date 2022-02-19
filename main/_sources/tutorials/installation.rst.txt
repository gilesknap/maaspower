.. _install:

Installation
============

Check your version of python
----------------------------

You will need python 3.8 or later. You can check your version of python by
typing into a terminal::

    python3 --version


Create a virtual environment
----------------------------

It is recommended that you install into a “virtual environment” so this
installation will not interfere with any existing Python software::

    python3 -m venv /path/to/venv
    source /path/to/venv/bin/activate


Running the application
-----------------------

You can now use ``pip`` to install the application::

    python3 -m pip install maaspower

If you require a feature that is not currently released you can also install
from github::

    python3 -m pip install git+git://github.com/gilesknap/maaspower.git

The application should now be installed and the command line interface on your path.
You can check the version that has been installed by typing::

    maaspower --version
