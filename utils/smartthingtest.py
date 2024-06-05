import asyncio

import aiohttp
from pysmartthings import SmartThings

print(
    "If you do not have an API key, generate"
    " one here: https://account.smartthings.com/tokens"
)

key = input("\nPlease enter the smartthings API key:\n")
device_id = input("Please enter the device network ID (blank for ALL):\n")
print()


async def switch():
    async with aiohttp.ClientSession() as session:
        api = SmartThings(session, key)
        devices = await api.devices()
        if len(devices) == 0:
            print("no devices for that API key")
        for device in devices:
            print("found device: ", device.device_id, device.name, device.label)
            if device.device_id == device_id or device_id == "":
                await device.status.refresh()
                print(" device status is :" + device.status.values.get("switch", ""))


asyncio.run(switch())
