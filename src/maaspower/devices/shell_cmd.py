"""
Classes to represent the configuration and functionality for devices
that can be controlled via a command line utility.

e.g. smart power switching usb hubs https://github.com/mvp/uhubctl
"""
from dataclasses import dataclass
from typing import Literal

from typing_extensions import Annotated as A

from maaspower.maasconfig import SwitchDevice

from ..globals import desc


@dataclass
class CommandLine(SwitchDevice):
    """A device controlled via SmartThings"""

    type: Literal["CommandLine"] = "CommandLine"
