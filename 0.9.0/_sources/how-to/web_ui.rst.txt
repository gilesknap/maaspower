.. _netgear:

Netgear GS308EP PoE 8 port switch
---------------------------------

I have successfully powered 3 RPIs with this device, but it should have no
issue powering a full 7 (with one port for uplink).


.. image:: ../images/netgear.png
  :width: 600
  :alt: GS803EP

In order to use this you will require PoE hat for your RPIs. I have used the 
official PoE v2 hat https://thepihut.com/products/raspberry-pi-poe-plus-hat.
But any would probably do.

IMPORTANT: I have yet to discover how to make the cooling fan work on this 
device. It is challenging because we have used MAAS to install a generic
version of Ubuntu without specific RPI device support. It is also not 
possible to use a passive cooling case with the hat in place. For this reason
I suggest that you provide some external cooling for a cluster built this 
way e.g. 

- https://thepihut.com/collections/raspberry-pi-cases/products/8-slot-cloudlet-cluster-case



.. image:: ../images/poehat.png
  :width: 400
  :alt: PoE









