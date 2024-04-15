"""
kasa_device.py
--------------

This module contains the class to represent and control TP-Link Kasa smart devices via
the python-kasa API. It provides functionalities to turn the device on or off
and to query its current state.
"""

import asyncio
from dataclasses import dataclass, field
from kasa import SmartPlug, SmartDeviceException
from typing_extensions import Annotated as A, Literal

from maaspower.maas_globals import desc
from maaspower.maasconfig import SwitchDevice


@dataclass(kw_only=True)
class KasaDevice(SwitchDevice):
    ip_address: A[str, desc("The IP address of the Kasa device.")]
    type: Literal["KasaDevice"] = "KasaDevice"
    name: A[str, desc("The name of the switching device.")]
    plug: SmartPlug = field(
        init=False
    )  # The SmartPlug instance is initialized in __post_init__.

    def __post_init__(self):
        """Initialize the smart plug with the provided IP address
        after the object is instantiated."""
        super().__post_init__()
        self.plug = SmartPlug(self.ip_address)

    def turn_on(self) -> None:
        """Asynchronously turn the smart plug on using a coroutine
        managed by asyncio."""
        asyncio.run(self._turn_on())

    async def _turn_on(self):
        """Private coroutine to turn the smart plug on, catching
        and logging any exceptions."""
        try:
            await self.plug.update()
            await self.plug.turn_on()
        except SmartDeviceException as e:
            print(f"Failed to turn on the smart plug at {self.ip_address}: {str(e)}")

    def turn_off(self) -> None:
        """Asynchronously turn the smart plug off using a coroutine
        managed by asyncio."""
        asyncio.run(self._turn_off())

    async def _turn_off(self):
        """Private coroutine to turn the smart plug off, catching
        and logging any exceptions."""
        try:
            await self.plug.update()
            await self.plug.turn_off()
        except SmartDeviceException as e:
            print(f"Failed to turn off the smart plug at {self.ip_address}: {str(e)}")

    def query_state(self) -> str:
        """Asynchronously query the current state of the smart plug
        and return it as 'on' or 'off'."""
        return asyncio.run(self._query_state())

    async def _query_state(self) -> str:
        """Private coroutine to query the state of the smart plug,
        returning 'on', 'off', or 'error' if an exception occurs."""
        try:
            await self.plug.update()
            return "on" if self.plug.is_on else "off"
        except SmartDeviceException as e:
            print(
                f"Failed to query state of the smart plug \
                    at {self.ip_address}: {str(e)}"
            )
            return "error"
