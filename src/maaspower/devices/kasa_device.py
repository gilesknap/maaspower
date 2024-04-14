"""
kasa_device.py
--------------

Classes to represent the configuration and functionality for TP-Link Kasa smart devices
that can be controlled via the python-kasa API.
"""

import asyncio
from dataclasses import dataclass
from kasa import SmartPlug
from typing_extensions import Annotated as A, Literal
from maaspower.maas_globals import desc
from maaspower.maasconfig import SwitchDevice


@dataclass(kw_only=True)
class KasaDevice(SwitchDevice):
    ip_address: A[str, desc("IP address of the Kasa device")]
    type: Literal["KasaDevice"] = "KasaDevice"
    name: A[str, desc("A name for the switching device")]

    def __post_init__(self):
        super().__post_init__()
        self.plug = None

    async def _initialize_plug(self):
        """Initialize the smart plug if it hasn't been initialized already."""
        if not self.plug:
            self.plug = SmartPlug(self.ip_address)
            await self.plug.update()

    def turn_on(self) -> None:
        """Asynchronously turn the smart plug on."""
        asyncio.run(self._turn_on())

    async def _turn_on(self):
        await self._initialize_plug()
        await self.plug.turn_on()

    def turn_off(self) -> None:
        """Asynchronously turn the smart plug off."""
        asyncio.run(self._turn_off())

    async def _turn_off(self):
        await self._initialize_plug()
        await self.plug.turn_off()

    def query_state(self) -> str:
        """Asynchronously query the current state of the smart plug."""
        return asyncio.run(self._query_state())

    async def _query_state(self) -> str:
        await self._initialize_plug()
        await self.plug.update()
        return "on" if self.plug.is_on else "off"
