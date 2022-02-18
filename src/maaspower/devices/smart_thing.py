"""
Classes to represent the configuration and functionality for devices
that can be controlled via the SmartThings API.

See https://www.smartthings.com/
"""
import asyncio
from dataclasses import dataclass
from typing import Literal

import aiohttp
from pysmartthings import SmartThings
from typing_extensions import Annotated as A

from maaspower.maasconfig import SwitchDevice

from ..globals import MaasResponse, desc


@dataclass
class SmartThing(SwitchDevice):
    """A device controlled via SmartThings"""

    type: Literal["SmartThingDevice"] = "SmartThingDevice"

    api_token: A[
        str,
        desc(
            "user account's API token for smart things "
            "see https://account.smartthings.com/login"
        ),
    ] = "none"

    device_id: A[
        str,
        desc("The identifier for the individual device"),
    ] = "none"

    def turn_on(self):
        print("turn on", self.on)
        asyncio.run(self.switch(self.on))
        return MaasResponse.ok

    def turn_off(self):
        print("turn off", self.off)
        asyncio.run(self.switch(self.off))
        return MaasResponse.ok

    def query_state(self):
        print("query", self.query)
        result = asyncio.run(self.switch(self.query, True))
        if result:
            return MaasResponse.on
        else:
            return MaasResponse.off

    async def switch(self, cmd: str, query: bool = False):
        async with aiohttp.ClientSession() as session:
            command = cmd.split(" ")

            api = SmartThings(session, self.api_token)
            devices = await api.devices()
            for device in devices:
                if device.device_id == self.device_id:
                    if query:
                        await device.status.refresh()
                        switch_state = device.status.values.get(command[0])
                        if switch_state == command[1]:
                            result = True
                        elif switch_state == command[2]:
                            result = False
                        else:
                            raise ValueError("unknown device state")
                    else:
                        await device.command(*command)
                        result = True
                break
            else:
                raise ValueError("Device not know to smartThings")

            return result
