Notes on Using a PoE switch With maaspower
==========================================

I plan to add a PoE switch power type to maaspower, which will likely
involve webscraping the management interface.

Candidates for PoE to the RPIs
- No need to look further:
- https://thepihut.com/products/raspberry-pi-poe-plus-hat
- plus matching case:
- https://thepihut.com/products/poe-hat-case-for-raspberry-pi-4

Some candidates for switches
- https://eu.store.ui.com/collections/unifi-network-routing-switching/products/unifi-switch-lite-8-poe
  
  - no details of the API or even if they can power switch ports
  - 8 ports for an OK good price
  - according to this post it can be CLI controlled via SSH 
    https://community.ui.com/questions/Need-to-be-able-to-toggle-power-on-ports-of-a-POE-switch/2545782f-0938-4b12-937c-24818a1957e6
    
- https://www.amazon.co.uk/TP-Link-TL-SG1005P-Ethernet-Configuration-Required/dp/B0769C24T1?th=1
  
  - awesome value, this is probably not switchable though
- https://www.amazon.co.uk/NETGEAR-Gigabit-Ethernet-Unmanaged-Network/dp/B08P54XZSJ/ref=pd_lpo_1?pd_rd_i=B09178VJK9&th=1
  
  - looks good for #57
- https://www.broadbandbuyer.com/products/35019-zyxel-gs1200-5hpv2-gb0101f/
- https://www.amazon.co.uk/dp/B08P53DL46?psc=1&smid=A2F15VRCPPJB05&ref_=chk_typ_imgToDp
  
  - Bought this one