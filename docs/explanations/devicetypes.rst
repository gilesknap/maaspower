Supported Types of Device Control
=================================

Examples
--------

This project has been tested against several power control devices. These specific examples have their own documentation pages as follows:

- `TP-Link Tapo Smart Plug<tapo>` - Command line example
- `UUGear MEGA4 USB Hub<mega4>` - SmartThings example
- `Netgear GS803EP PoE 8 port switch<netgear>`  - Web GUI example
- `TP-Link Kasa Smart Plug<kasa>` - Python-Kasa API example

Kasa Device Control
-------------------

:example:
    `TP-Link Kasa Smart Plug<kasa>`

Kasa devices are controlled using the Python-Kasa library which interfaces 
with TP-Link Kasa smart devices over the network. This method involves 
asynchronous communication with devices to execute actions like turning 
on or off and querying their current state.

An example configuration for controlling a Kasa smart plug is shown below:

:example yaml:

.. code-block:: yaml

        - type: KasaDevice
            name: server01_plug
            ip_address: 192.168.1.100
            on: "python -m kasa --host 192.168.1.100 on"
            off: "python -m kasa --host 192.168.1.100 off"
            query: "python -m kasa --host 192.168.1.100 state"


This configuration uses the Python-Kasa API to communicate with the plug. 
The `ip_address` should be replaced with the IP address of your Kasa device. 
The `on`, `off`, and `query` commands are examples of how you might invoke 
device control through command line interfacing with the Python-Kasa library.

.. note::
    Ensure that the `python-kasa` library is installed in the environment 
    where your server is running, as it is required for communication 
    with Kasa devices.



Command Line Control
--------------------

:example:
    `TP Link Tapo Smart Plug<tapo>`

The simplest form of control is to execute a command line utility. Clearly 
the command tool needs to be installed on the machine running the webhook
server, the server account needs permission to run it and the tool must
be able to contact the device from the server.

A common example for RPI power is a switchable USB hub. Most of these can be
controlled by the uhubctl command line tool. 
(see https://github.com/mvp/uhubctl).

Using uhubctl implies that the hub in question is plugged into a USB port
on the webhook server.

:example yaml:

.. code-block:: yaml

        - type: CommandLine
            name: pi2
            on: uhubctl -a 1 -p 2
            off: uhubctl -a 0 -p 2
            query: uhubctl -p 2
            query_on_regex: .*power$
            query_off_regex: .*off$


SmartThings Control
-------------------

:example:
    `TP Link Tapo Smart Plug<tapo>`

SmartThings are IoT devices
which are controlled using a SmartThing api token and SmartThing device
ID. Once you have set up a SmartThing and tested it via the associated 
App you will be able to discover your device ID via the App. You can get
your api token by logging in here: https://account.smartthings.com/login.


Note that the ip_address of 0.0.0.0 tells the server to listen on all
interfaces on the machine on which it is running. Instead one could
supply the IP of a single NIC or for best security use 127.0.0.1, meaning
that only processes on the same machine will have access (in this cases
you would run the webhook server on the maas rack server).

SmartThing commands for switch devices will usually take the exact same form 
as in the above example. Command line devices will just take a command line 
to execute in the shell.

In all cases the response from the query command is passed through a regex search
and will return 'on' if the the response matches query_on_regex and 'off' it
matches query_off_regex. Note that the defaults for these regex are 'on' and
'off' which is what SmartThing devices will return in the switch 
status field by default. This is why the nuc1 example is not required to 
specify query_on_regex, query_off_regex.

Note that the query response which goes to MAAS is converted to 
MAAS default values and hence no configuration of regex in 
MAAS itself are required.

example yaml:

.. code-block:: yaml

        - type: SmartThingDevice
            name: nuc1
            # token and id redacted
            api_token: YOUR_SMART_THINGS_API_TOKEN
            device_id: YOUR_SMART_THING_DEVICE_ID
            off: main switch off
            on: main switch on
            query: switch

Web GUI Control
---------------

:example:
    `Netgear GS803EP PoE 8 port switch<netgear>`

For those power control devices that are configured by a web UI only, I provide
a Web Scraping device type. This uses the python selenium library to 
click buttons and send text to forms on any Web UI. Defining the correct
sequence should allow you to login to any Web GUI and control it.


Per Control Device Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this device type there are two types of entry. First is the global entry
where you configure how to connect/disconnect to/from each device. (i.e.
if you had 2 PoE switches you would have 2 of these) 

example WebGui yaml:

.. code-block:: yaml

        - type: WebGui
            name: GS308EP
            connect_url: http://GS308EP_IP_ADDRESS
            timeout: 10
            driver: /home/giles/work/maaspower/utils/chromedriver
            login: |
                sendcr/cls/pwd-field-text/PASSWORD_GOES_HERE
                click/link/POE
            logout: |
                click/cls/src-views-header-nav-icon-button
                click/cls/icon-logout
                click/id/modal_footer_button_primary

You will need the chromedriver for selenium for this to work. Download from 
here (pick one that matches your Chrome version):

- https://chromedriver.storage.googleapis.com/index.html

The configuration 'driver:' needs to point at the downloaded file. 'timeout:'
should be the max time taken for any transitions in the click sequences you 
specify. 

'login:' and 'logout': specify the sequence of clicks to perform these two 
tasks.

The configuration strings are '/' separated fields as follows:

Commands
@@@@@@@@

:click/...   
    clicks on the specified HTML Element

send/.../text_to_send
    sends text to a specified HTML Element

sendcr/.../text_to_send
    sends text plus carriage return to a specified HTML Element

get/...   
    gets the text from a specified HTML Element

delay/n   
    pauses for n seconds (floating point supported)

Field Identifiers
@@@@@@@@@@@@@@@@@

The second and third parts of the / separated strings identify the HTML
Element to target:

n/value
    finds the fields whose name is 'value'

cls/value
    finds the fields whose class is 'value'

link/value
    find the fields with link contents specified by a partial match on 'value'

id/value
    find the fields whose id is 'value'


NOTE: in all cases if more than one field is matched you can index it like this:

    command/match_type/value[n]

Where n is the 0 based index into the list of fields.

NOTE: in all cases the code will wait for the specified field to be seen
if it cannot immediately be seen. 
'timeout' specifies the maximum wait time before an error.

When the web scraper detects an error it will execute the logout script
(ignoring errors) followed by the login script and try again. This has 
been shown to successfully recover on the GS308EP when it has timed out
due to inactivity and gone back to the login screen.



Per Control Device Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each computer that you want to power control you will need an additional
entry like the following example. On, Off and Query use the same syntax as 
described above. 

Note that the name has the entry above's name followed by a computer name 
separated by '-' this is important as it associates this entry with the 
correct Web Device. Only one instance of the selenium driver is loaded 
per web device and can control any number of target PCs.

The _regex parameters are regular expressions which will try to match
the text returned from the final get in the query sequence. If there is 
a match it will return on or off to MAAS, or an error if there is none.

example WebDevice yaml:

.. code-block:: yaml

    - type: WebDevice
        name: GS308EP-pi5
        on: |
            click/n/isShowPot3
            click/n/editPot3
            click/cls/poePortPwrTxt
            click/link/Enable
            click/n/submitPotedit
        off: |
            click/n/isShowPot3
            click/n/editPot3
            click/cls/poePortPwrTxt
            click/link/Disable
            click/n/submitPotedit
        query: |
            delay/5
            get/cls/portPwr[2]
        query_on_regex: Enable
        query_off_regex: Disable


Working with another Web GUI
----------------------------

This has been tested with the Netgear GS3008EP. I have tried to make a generic
DSL that allows for most possible sequences of Web Element interactions, but 
YMMV. 

To experiment with the approach and develop your own command sequences for
this device type see the python script here: 
https://github.com/gilesknap/maaspower/blob/main/utils/webuitest.py
You can launch this script interactively with iPython and experiment with
your device to get the right sequence of commands to turn devices on/off and
query their state. See the comments in the file for details.

If you are brave enough to create your own config for a new device, please
report any problems here https://github.com/gilesknap/maaspower/issues. Also
post any working configurations too (you can do a PR to the docs or 
report in issues).


