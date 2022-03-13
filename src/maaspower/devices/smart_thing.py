"""
smart_thing.py
--------------

Classes to represent the configuration and functionality for devices
that can be controlled via the SmartThings API.

See https://www.smartthings.com/
"""
import asyncio
from dataclasses import dataclass

import aiohttp
from pysmartthings import SmartThings
from typing_extensions import Annotated as A
from typing_extensions import Literal

from maaspower.maasconfig import SwitchDevice

from ..globals import desc


@dataclass
class SmartThing(SwitchDevice):
    """A device controlled via SmartThings"""

    type: Literal["SmartThingDevice"] = "SmartThingDevice"

    api_token: A[
        str,
        desc("SmartThings API token see https://account.smartthings.com/login"),
    ] = "none"

    device_id: A[
        str,
        desc("The SmartThings identifier for an individual device"),
    ] = "none"

    def turn_on(self):
        asyncio.run(self.switch(self.on))

    def turn_off(self):
        asyncio.run(self.switch(self.off))

    def query_state(self) -> str:
        return asyncio.run(self.switch(self.query, True))

    async def switch(self, cmd: str, query: bool = False):
        async with aiohttp.ClientSession() as session:
            result = ""

            api = SmartThings(session, self.api_token)
            devices = await api.devices()
            for device in devices:
                if device.device_id == self.device_id:
                    if query:
                        await device.status.refresh()
                        result = device.status.values.get(cmd)
                    else:
                        # commands are space separated sequences of identifiers
                        command = cmd.split(" ")
                        await device.command(*command)
                    break
            else:
                raise ValueError("Device not know to smartThings")

            return result
