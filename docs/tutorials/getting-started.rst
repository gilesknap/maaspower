How to use MaasPower
====================

To use maaspower you will first need to create a configuration file that
describes the set of devices that you want to control and the webhooks that
will be supplied to control them.

Next launch the webhook server on an appropriate machine.

Finally configure MAAS to talk to the webhook server on behalf of each of the
bare metal machines that you are controlling.

Configuration
-------------

An example YAML config file is shown below. This configures the following
devices, which include all device types currently supported

- A SmartThings controlled device, nuc1.
- 2 Command line controlled devices pi1, p2.
- A Web GUI controlled device, pi5.

    .. highlight:: yaml

    .. include:: ../../tests/samples/sampleconfig.yaml
        :literal:


Launch the Web Hook server
--------------------------

Once you have the correct configuration you can launch the server from
the command line. This assumes you have activated a virtual environment
with maaspower installed, see `installation`.

It is important to select an appropriate machine to run the Web Hook Server.
First if there are any usb controlled hubs or other devices that are not
network attached then the Web Server must run on the machine with these devices
connected. A good option is to use a rack server and have all the necessary
hardware connected to it.

Use this command::

    maaspower run <path to configuration file>

This command will validate your config file against the schema and report
any issues. Schema validation failure will abort the web server.

If you wish to get assistance with the format of the config file you can
generate a schema file and use a schema aware editor which will give you
hints and autocompletion. See `yaml_schema` for details.

Configure MAAS to connect to the webhook
----------------------------------------

For each device configured in the maaspower config file. There needs to be
an equivalent configuration of a MAAS controlled machine.

To do this select a Machine in the MAAS Web GUI and go to the configuration
tab. Then select Power Configuration -> Edit.

An example configuration that matches the nuc1 device in the above config
file is shown below. In this example the Webhook Server has been launched
on a machine with IP 192.168.0.1.

.. image:: ../images/MaasGuiSettings.png
  :width: 600
  :alt: Alternative text

