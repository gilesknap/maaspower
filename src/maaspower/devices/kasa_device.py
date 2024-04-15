"""
kasa_device.py
--------------

Classes to represent the configuration and functionality for TP-Link Kasa smart devices
that can be controlled via the python-kasa API.
"""

import asyncio
import threading
from dataclasses import dataclass, field
from typing_extensions import Annotated as A, Literal
from kasa import SmartPlug, SmartDeviceException

from maaspower.maas_globals import desc
from maaspower.maasconfig import SwitchDevice


def run_async(func):
    """
    Decorator to run an async function in a new thread with its own event loop.
    """

    def wrapper(*args, **kwargs):
        def inner():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(func(*args, **kwargs))
            finally:
                loop.close()

        thread = threading.Thread(target=inner)
        thread.start()
        return thread

    return wrapper


@dataclass(kw_only=True)
class KasaDevice(SwitchDevice):
    ip_address: A[str, desc("IP address of the Kasa device")]
    type: Literal["KasaDevice"] = "KasaDevice"
    plug: SmartPlug = field(default_factory=lambda: None)

    def __post_init__(self):
        self.plug = SmartPlug(self.ip_address)

    @run_async
    async def turn_on(self) -> None:
        """Turns on the smart plug asynchronously."""
        await self._async_switch(True)

    @run_async
    async def turn_off(self) -> None:
        """Turns off the smart plug asynchronously."""
        await self._async_switch(False)

    @run_async
    async def query_state(self) -> str:
        """Queries the current state of the smart plug asynchronously."""
        return await self._async_query_power_status()

    async def _async_switch(self, turn_on: bool) -> None:
        """
        Internal method to handle turning the smart plug on or off asynchronously.
        Handles device state updates and executes the turn on/off command.
        """
        try:
            await self.plug.update()  # Make sure the plug's state is up to date
            if turn_on:
                await self.plug.turn_on()
            else:
                await self.plug.turn_off()
        except SmartDeviceException as e:
            print(f"Error operating the smart plug {self.ip_address}: {str(e)}")

    async def _async_query_power_status(self) -> str:
        """
        Internal method to asynchronously query the power status of the smart plug.
        Returns 'on' if the plug is on, 'off' if off, or 'error' if an exception occurred.
        """
        try:
            await self.plug.update()
            return "on" if self.plug.is_on else "off"
        except SmartDeviceException as e:
            print(f"Error querying the smart plug {self.ip_address}: {str(e)}")
            return "error"
