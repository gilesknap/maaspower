import asyncio
import time
from ast import Str
from ctypes import cast
from typing import List, Literal, Optional, Tuple

import aiohttp
from pysmartthings import Device, SmartThings


class HelloClass:
    """A class whose only purpose in life is to say hello"""

    def __init__(self, token):
        """
        Args:
            name: The initial value of the name of the person who gets greeted
        """
        #: The name of the person who gets greeted
        self.token = token

    def test(self):
        pass

    async def send_command(self, api: SmartThings, device_id: str, command: List[str]):
        devices = await api.devices()
        for device in devices:
            if device.device_id == device_id:
                await device.command(*command)
            print(device_id)
            break
        else:
            raise ValueError("Device not know")

    async def switch(self, on_off: str):
        async with aiohttp.ClientSession() as session:
            command = ["main", "switch", on_off]
            device_id = "1c72370a-885a-4485-9721-ffaf6586101b"
            try:
                api = SmartThings(session, self.token)
                await self.send_command(api, device_id, command)
            except Exception as e:
                print(f"command {command} in device {device_id} failed")
                print(str(e))

    def run_switch(self, on_off: str):
        asyncio.run(self.switch(on_off))


def run_test(token):
    h = HelloClass(token)
    h.run_switch("off")
    time.sleep(1)
    h.run_switch("on")
