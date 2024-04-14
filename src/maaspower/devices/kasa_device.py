"""
kasa_device.py
--------------

Classes to represent the configuration and functionality for TP-Link Kasa smart devices
that can be controlled via the python-kasa API.
"""

import asyncio
import re
from dataclasses import dataclass
from kasa import SmartPlug
from typing_extensions import Annotated as A, Literal
from maaspower.maas_globals import desc
from maaspower.maasconfig import RegexSwitchDevice, MaasResponse


@dataclass(kw_only=True)
class KasaDevice(RegexSwitchDevice):
    ip_address: A[str, desc("IP address of the Kasa device")]
    type: Literal["KasaDevice"] = "KasaDevice"

    async def initialize_plug(self):
        """Initialize the smart plug."""
        self.plug = SmartPlug(self.ip_address)
        await self.plug.update()  # Load initial data

    async def turn_on(self):
        """Turn the smart plug on."""
        await self.plug.turn_on()
        await self.plug.update()

    async def turn_off(self):
        """Turn the smart plug off."""
        await self.plug.turn_off()
        await self.plug.update()

    async def query_state_async(self):
        """Query the current state of the smart plug."""
        await self.plug.update()
        return "on" if self.plug.is_on else "off"

    def run_query(self) -> str:
        """Synchronously wraps the async method to query the plug's state."""
        result = asyncio.run(self.query_state())
        return result

    def query_state(self) -> str:
        """Uses regex patterns to ascertain the correct response."""
        query_response = self.run_query()
        if re.search(self.query_on_regex, query_response, flags=re.MULTILINE):
            return MaasResponse.on.value
        elif re.search(self.query_off_regex, query_response, flags=re.MULTILINE):
            return MaasResponse.off.value
        else:
            raise ValueError(
                f"Unknown power state response: \n{query_response}\n"
                f"\nfor regexes {self.query_on_regex}, {self.query_off_regex}"
            )
