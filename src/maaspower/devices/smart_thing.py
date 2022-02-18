"""
Classes to represent the configuration and functionality for devices
that can be controlled via the SmartThings API.

See https://www.smartthings.com/
"""
from dataclasses import dataclass
from typing import Literal

from typing_extensions import Annotated as A

from maaspower.config import SwitchDevice

from ..globals import desc


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
