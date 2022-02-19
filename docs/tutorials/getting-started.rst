Getting Started
===============

To use maaspower you will first need to create a configuration file that 
describes the set of devices that you want to control and the webhooks that
will be supplied to control them.

An example YAML config file is shown here. This configures 1 SmartThings
switched power socket and 2 devices connected to the same switching USB
power Hub. The example power hub is controlled via the uhubctl command line
tool (see https://github.com/mvp/uhubctl). 
Click the arrow to expand the example.

    .. raw:: html

        <details>
        <summary><a>sampleconfig.yaml</a></summary>

    .. highlight:: yaml

    .. include:: ../../tests/samples/sampleconfig.yaml
        :literal:

    .. raw:: html

        </details>

Once you have the correct configuration you can launch the server from
the command line. This assumes you have activated a virtual environment
with maaspower installed, see `install`.

Use this command::

    maaspower run <path to configuration file>

TOOO: continue here with more detail and cover schema validation