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
from maaspower.maasconfig import RegexSwitchDevice


@dataclass(kw_only=True)
class KasaDevice(RegexSwitchDevice):
    """A device controlled via python-kasa, specifically for TP-Link Kasa smart plugs."""

    ip_address: A[str, desc("IP address of the Kasa device")]
    type: Literal["KasaDevice"] = "KasaDevice"

    async def initialize_plug(self):
        """Initialize the smart plug."""
        self.plug = SmartPlug(self.ip_address)
        await self.plug.update()  # Load initial data

    async def turn_on(self):
        """Turn the smart plug on."""
        await self.plug.turn_on()
        await self.plug.update()  # Optional, to refresh state immediately

    async def turn_off(self):
        """Turn the smart plug off."""
        await self.plug.turn_off()
        await self.plug.update()  # Optional, to refresh state immediately

    async def query_state(self):
        """Query the current state of the smart plug."""
        await self.plug.update()  # Ensure the state is current
        return "on" if self.plug.is_on else "off"

    def run_query(self) -> str:
        """Synchronously wrap the async query_state method for compatibility."""
        result = asyncio.run(self.query_state())
        return result
