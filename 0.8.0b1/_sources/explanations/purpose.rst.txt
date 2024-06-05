Purpose of this Package
=======================

Canonical's Metal As A Service (MAAS) commissions and deploys bare metal machines
automatically, see https://maas.io/. It uses PXE boot so any machine that
can network boot can theoretically be managed with MAAS.

However, MAAS does need to be able to remotely power cycle a machine in order 
to complete its function. Data centre machines will all have a BMC that
allows for this but consumer machines rarely do.

MAAS allows for this by allowing a Web Hook to be configured for power
cycling each machine. All you need is some remotely controlled power supply
for your machine and some software that provides a web hook understood by MAAS,
and responds to the web hook by powering on/off the machine. 

Each machine will need 3 web hooks:

- power on
- power off
- query power state

This python package can stand up multiple web hooks and connect them to a 
variety of back end remote control devices. The package has an extensible 
architecture and at present supports two types of backend which will cover
a large number of devices. The backends supported are:

- SmartThings API: a popular Samsung IoT protocol that is supported by 
  thousands of devices
- Command line interface. Anything that is controllable by a command line 
  utility that can be installed on the machine running this webhook service. 