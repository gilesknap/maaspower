"""
Classes to represent the configuration and functionality for devices
that can be controlled via the SmartThings API.

See https://www.smartthings.com/
"""
from dataclasses import dataclass
from typing import Literal

from typing_extensions import Annotated as A

from maaspower.maasconfig import SwitchDevice

from ..globals import desc


@dataclass
class SmartThing(SwitchDevice):
    """A device controlled via SmartThings"""

    api_token: A[
        str,
        desc(
            "user account's API token for smart things "
            "see https://account.smartthings.com/login"
        ),
    ]

    device_id: A[
        str,
        desc("The identifier for the individual device"),
    ]

    on: A[str, desc("space separated command tree to switch device on")]
    off: A[str, desc("space separated command tree  to switch device off")]
    query: A[str, desc("the command to query device state")]

    type: Literal["SmartThingDevice"] = "SmartThingDevice"
