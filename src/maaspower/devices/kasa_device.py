"""
kasa_device.py
--------------

Classes to represent the configuration and functionality for TP-Link Kasa smart devices
that can be controlled via the python-kasa API.
"""

import asyncio
from dataclasses import dataclass
from typing_extensions import Annotated as A, Literal
from kasa import SmartPlug, SmartDeviceException
from maaspower.maas_globals import desc
from maaspower.maasconfig import SwitchDevice


@dataclass(kw_only=True)
class KasaDevice(SwitchDevice):
    """A device controlled via python-kasa,
    specifically for TP-Link Kasa smart plugs."""

    ip_address: A[str, desc("IP address of the Kasa device")]
    type: Literal["KasaDevice"] = "KasaDevice"
    plug: SmartPlug = None

    def __post_init__(self):
        self.plug = SmartPlug(self.ip_address)

    def turn_on(self) -> None:
        """Turns on the smart plug."""
        asyncio.run(self._async_switch(True))

    def turn_off(self) -> None:
        """Turns off the smart plug."""
        asyncio.run(self._async_switch(False))

    def query_state(self) -> str:
        """Queries the current state of the smart plug."""
        return asyncio.run(self._async_query_power_status())

    async def _async_switch(self, turn_on: bool) -> None:
        """Internal method to handle turning the smart plug on or off asynchronously."""
        try:
            await self.plug.update()  # Ensure the device's state is current before changing it
            if turn_on:
                await self.plug.turn_on()
            else:
                await self.plug.turn_off()
        except SmartDeviceException as e:
            # Log the exception or handle it as needed
            print(f"Error controlling device {self.ip_address}: {str(e)}")

    async def _async_query_power_status(self) -> str:
        """Internal method to asynchronously query the power status of the smart plug."""
        try:
            await self.plug.update()
            return "on" if self.plug.is_on else "off"
        except SmartDeviceException as e:
            # Log the exception or handle it as needed
            print(f"Error querying device {self.ip_address}: {str(e)}")
            return "error"
