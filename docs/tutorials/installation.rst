.. _install:

Installation
============


Install using python and pip
----------------------------

Check your version of python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need python 3.8 or later. You can check your version of python by
typing into a terminal::

    python3 --version


Create a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is recommended that you install into a “virtual environment” so this
installation will not interfere with any existing Python software::

    python3 -m venv /path/to/venv
    source /path/to/venv/bin/activate


Running the application
~~~~~~~~~~~~~~~~~~~~~~~

You can now use ``pip`` to install the application::

    # first make sure pip and wheel are up to date
    python3 -m pip install --upgrade pip wheel
    python3 -m pip install maaspower

If you require a feature that is not currently released you can also install
from github::

    python3 -m pip install git+git://github.com/gilesknap/maaspower.git

The application should now be installed and the command line interface on your path.
You can check the version that has been installed by typing::

    maaspower --version


Install using the container
---------------------------

Releases of MaasPower include a container that holds python, maaspower and
also the uhubctl command line utility. This can be a convenient way to 
deploy since you will only need a container runtime on the target machine.

If you use docker you can tell it to restart the container on reboot of the
machine so this is a convenient way to install it as a 'service'.

Assuming you already have docker (or podman) installed then the following 
command line will launch maaspower as a background task and restart it
on reboot.

(replace CONFIG_FILE and CONFIG_PATH with your own config file details)


.. code-block:: bash

    volumes="-v <CONFIG_PATH>:/config"
    service="-d --restart unless-stopped"
    image="ghcr.io/gilesknap/maaspower:0.5"
    sudo="--privileged --net host"
    docker run -it --name maaspower $volumes $service $sudo $image run /config/<CONFIG_FILE>     

You can look at the output to verify all is well with:

.. code-block:: bash

    docker logs maaspower

And stop the web server with:


.. code-block:: bash

    docker stop maaspower
    docker container delete maaspower
