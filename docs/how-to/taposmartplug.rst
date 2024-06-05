.. _tapo:

TP Link Tapo Smart Plug
=======================

MaasPower has been tested with this device. It provides a remote switchable
power socket and could be used to control power switching on any machine.


.. image:: ../images/tapo.png
  :width: 400
  :alt: Alternative text

To use this device, first install the Tapo App on a phone, create an
account and register the device.

Also install the SmartThings App and create
an account.

You can now register your Tapo device as a SmartThing via
the 2nd App. As detailed here https://www.tapo.com/uk/faq/120/

The config requires an API Token which can be created by going to this URL:
https://account.smartthings.com/tokens.
The API Token can be reused for multiple devices.

You can now go into the SmartThings website at https://account.smartthings.com/.
On this site you will find the Device Network ID to supply in MaasPower's
config file. Go to the 'My Devices' tab and copy the id from the
'Device Network Id' column.

UPDATE: the Device Network ID shown on the website no longer correlates with
the ID used by the python library. I provide a small test utility to find
out the IDs of your Smarthings Devices. First make sure you have your
venv activated as described in `../tutorials/installation`. Then run the following commands:


.. code-block:: bash

    curl -O https://raw.githubusercontent.com/gilesknap/maaspower/main/utils/smartthingtest.py
    python smartthingtest.py

    # you will see this and supply your API key when prompted
    If you do not have an API key, generate one here: https://account.smartthings.com/tokens

    Please enter the smartthings API key:
    xxxxxx-xxxxxx-xxxxxx-xxxxxx
    Please enter the device network ID (blank for ALL):

found device:  ab9xxxxx-xxxx-xxxx-xxxx-xxxxx4199a0e c2c-switch Virgin Router
 device status is :on
found device:  a60xxxxx-axxxx-xxxx-xxxx-xxxxx778b82 c2c-switch nuc1 power
 device status is :on

Also Note that you can test your running WebHook Server with a command like
this:

.. code-block:: bash

    curl --user test_user:test_pass http://192.168.0.104:5000/maaspower/nuc1/query