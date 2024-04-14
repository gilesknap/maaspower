"""
kasa_device.py
--------------

Classes to represent the configuration and functionality for TP-Link Kasa smart devices 
that can be controlled via the python-kasa API.
"""

import asyncio
from dataclasses import dataclass

from kasa import SmartPlug
from typing_extensions import Annotated as A
from typing_extensions import Literal

from maaspower.maas_globals import desc
from maaspower.maasconfig import RegexSwitchDevice


@dataclass(kw_only=True)
class KasaDevice(RegexSwitchDevice):
    """A device controlled via python-kasa"""

    ip_address: A[str, desc("IP address of the Kasa device")]

    type: Literal["KasaDevice"] = "KasaDevice"

    def turn_on(self):
        asyncio.run(self.switch(True))

    def turn_off(self):
        asyncio.run(self.switch(False))

    def query_state(self) -> str:
        return asyncio.run(self.query_power_status())

    async def switch(self, turn_on: bool):
        plug = SmartPlug(self.ip_address)
        await plug.update()  # Refresh the latest state before sending command
        if turn_on:
            await plug.turn_on()
        else:
            await plug.turn_off()

    async def query_power_status(self) -> str:
        plug = SmartPlug(self.ip_address)
        await plug.update()
        return "on" if plug.is_on else "off"
