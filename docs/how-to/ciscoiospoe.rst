.. _ciscoiospoehowto:

Cisco IOS PoE Switches
======================

Maaspower has been tested with specific devices in this
category. So far, it has only been tested with a Cisco
Catalyst 2960X 24-port PoE+ switch (WS-C2960X-24PS-L), but
various Cisco IOS PoE switches should work with it.

.. image:: ../images/ciscoiospoeswitch.png
  :width: 600
  :alt: A Cisco Catalyst 2960X 24-port PoE+ Network Switch

To use this device, ensure SSH authentication is enabled on
the switch and that maaspower can reach its IP address. You
will need to either use a privileged user account (such as
the root account) or create an ``enable`` password and
specify it in the maaspower device config YAML.

Refer to `Cisco IOS PoE Switch Device Control
<ciscoiospoeconfig>` for more information and examples
on configuring a Cisco IOS switch for maaspower.