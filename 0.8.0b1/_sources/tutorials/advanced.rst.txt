Using Regular Expressions in Device Names
=========================================

Frequently there will be multiple similar devices to control with MaasPower.
To save on repetition in the configuration YAML it is possible to use
regular expressions for the device names and to have elements of the 
match against that expression be substituted into the command strings.

Simple Example
--------------

The substitution string \\g<0> will be replaced with the name of the 
device that matched the regex in all command strings. (Apologies for
the esoteric string - but this is a Python anomoly for regex since
\\0 has another meaning in python strings)

This example YAML snippet will match all device names of the form
"192_168_xxx_yyy" where xxx and yyy are 1 to 3 digits.

.. code-block:: yaml

    devices:
    - type: CommandLine
        name: '192_168_\d{1,3}_\d{1,3}'
        on: myscript.sh \g<0> on
        off: myscript.sh \g<0> off
        query: myscript.sh \g<0> query

The on, off and query command line definitions will all have the \\g<0>
substituted with the device name that was passed to the webhook server. 

For example posting to the URL:

.. code-block::

    http://localhost:5000/maaspower/192_168_1_2/on

would execute the shell command

.. code-block::  bash

    myscript.sh 192_168_1_2 on

Note that the name is enclosed in single quotes to allow escape 
sequences like '\\d'. Also it is best to try our your regular expressions
on a tool like regex101. For example see the above regex being tested 
here: https://regex101.com/r/tE982R/1.

Use of Capture Groups
---------------------

The text within capture group 1 will be used to replace the substitution string
\\1, group 2 is \\2 etc.

You can add capture groups to the regex by enclosing a section in round
brackets. See regex101 example here https://regex101.com/r/OMRHmF/1.
You can also use named capture groups if prefered and then the substitution
string would be \\p<name>.

The following example could support multiple uhubctl devices in a single
device YAML description.

    .. highlight:: yaml

    .. include:: ../../tests/samples/sampleregex2.yaml
        :literal:

There are two capture groups, the first captures 'raspi-XXX' where XXX is 1 or
more digits. The second captures a number to represent the uhubctl port for 
this device.

Note that in this case the commands need to be enclosed in single quotes to 
escape \\1 and \\2.

Hence posting to the URL:

.. code-block:: 

    http://localhost:5000/maaspower/raspi1-p1/on

would execute the shell command

.. code-block::  bash

    uhubctl -a 1 -p 1 # turn on raspi1 (full device name was raspi1-p1)

