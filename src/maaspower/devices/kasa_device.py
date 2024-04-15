"""
kasa_device.py
--------------

Classes to represent the configuration and functionality for TP-Link Kasa smart devices
that can be controlled via the python-kasa API.
"""

import asyncio
from dataclasses import dataclass
from kasa import SmartPlug, SmartDeviceException
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
            try:
                await self.plug.update()
            except SmartDeviceException as e:
                print(
                    f"Failed to initialize the smart plug at {self.ip_address}: {str(e)}"
                )
                raise

    def turn_on(self) -> None:
        """Asynchronously turn the smart plug on."""
        asyncio.run(self._turn_on())

    async def _turn_on(self):
        try:
            await self._initialize_plug()
            await self.plug.turn_on()
        except SmartDeviceException as e:
            print(f"Failed to turn on the smart plug at {self.ip_address}: {str(e)}")
            raise

    def turn_off(self) -> None:
        """Asynchronously turn the smart plug off."""
        asyncio.run(self._turn_off())

    async def _turn_off(self):
        try:
            await self._initialize_plug()
            await self.plug.turn_off()
        except SmartDeviceException as e:
            print(f"Failed to turn off the smart plug at {self.ip_address}: {str(e)}")
            raise

    def query_state(self) -> str:
        """Asynchronously query the current state of the smart plug."""
        return asyncio.run(self._query_state())

    async def _query_state(self) -> str:
        try:
            await self._initialize_plug()
            await self.plug.update()
            return "on" if self.plug.is_on else "off"
        except SmartDeviceException as e:
            print(
                f"Failed to query state of the smart plug at {self.ip_address}: {str(e)}"
            )
            return "error"
