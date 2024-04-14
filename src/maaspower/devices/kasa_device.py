"""
kasa_device.py
--------------

Classes to represent the configuration and functionality for TP-Link Kasa smart devices
that can be controlled via the python-kasa API.
"""

import asyncio
import threading
from dataclasses import dataclass, field
from kasa import SmartPlug
from typing_extensions import Annotated as A, Literal

from maaspower.maas_globals import desc
from maaspower.maasconfig import SwitchDevice


def run_async(func):
    """
    Helper function to run an async function using threading.
    """

    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func(*args, **kwargs))
        loop.close()

    return wrapper


@dataclass(kw_only=True)
class KasaDevice(SwitchDevice):
    ip_address: A[str, desc("IP address of the Kasa device")]
    type: Literal["KasaDevice"] = "KasaDevice"
    plug: SmartPlug = field(init=False)

    def __post_init__(self):
        self.plug = SmartPlug(self.ip_address)

    def turn_on(self) -> None:
        threading.Thread(target=run_async(self._async_switch), args=(True,)).start()

    def turn_off(self) -> None:
        threading.Thread(target=run_async(self._async_switch), args=(False,)).start()

    def query_state(self) -> str:
        return asyncio.run(self._async_query_power_status())

    async def _async_switch(self, turn_on: bool) -> None:
        await self.plug.update()
        if turn_on:
            await self.plug.turn_on()
        else:
            await self.plug.turn_off()

    async def _async_query_power_status(self) -> str:
        await self.plug.update()
        return "on" if self.plug.is_on else "off"
