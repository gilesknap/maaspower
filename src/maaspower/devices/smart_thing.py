"""
Classes to represent the configuration and functionality for devices
that can be controlled via the SmartThings API.

See https://www.smartthings.com/
"""
import asyncio
from dataclasses import dataclass
from typing import Literal

import aiohttp
from pysmartthings import Device, SmartThings
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
        return MaasResponse.ok

    def turn_off(self):
        print("turn off", self.off)
        return MaasResponse.ok

    def query_state(self):
        print("query", self.query)
        return MaasResponse.on
