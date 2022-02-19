"""
massconfig.py
-------------

This module uses APISchema to serialize and deserialize the config
file, plus provides a schema for easy editing of the config.


The MaasConfig class plus SwitchDevice derived classes in the devices folder
provide an in memory representation of the contents of
the maaspower YAML configuration file that specifies the set of power
manager devices for which to serve web hooks.
"""

import re
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Type

from apischema import deserialize, identity
from apischema.conversions import Conversion, deserializer
from typing_extensions import Annotated as A

from .globals import MaasResponse, T, desc


@dataclass
class SwitchDevice:
    """
    A base class for the switching devices that the webhook server will control.
    Concrete subclasses are found in the devices subfolder
    """

    name: A[str, desc("A name for the switching device")]

    on: A[str, desc("command line string to switch device on")]
    off: A[str, desc("command line string to switch device off")]
    query: A[str, desc("command line string to query device state")]
    query_on_regex: A[str, desc("match the on status return from query")] = "on"
    query_off_regex: A[str, desc("match the off status return from query")] = "off"

    description: A[Optional[str], desc("A description of the device")] = ""
    type: str = "none"  # a literal to distinguish the subclasses of Device

    # https://wyfo.github.io/apischema/examples/subclass_union/
    def __init_subclass__(cls):
        # Deserializers stack directly as a Union
        deserializer(Conversion(identity, source=cls, target=SwitchDevice))

    # command functions to be implemented in the derived classes
    def turn_on(self) -> None:
        raise (NotImplementedError)

    def turn_off(self) -> None:
        raise (NotImplementedError)

    def query_state(self) -> str:
        raise (NotImplementedError)

    def do_command(self, command) -> Optional[str]:
        result = None

        if command == "on":
            self.turn_on()
        elif command == "off":
            self.turn_off()
        elif command == "query":
            query_response = self.query_state()
            if re.search(self.query_on_regex, query_response, flags=re.MULTILINE):
                result = MaasResponse.on.value
            elif re.search(self.query_off_regex, query_response, flags=re.MULTILINE):
                result = MaasResponse.off.value
            else:
                raise ValueError(
                    f"Unknown power state response: \n{query_response}\n"
                    f"\nfor regexes {self.query_on_regex}, {self.query_off_regex}"
                )
        else:
            raise ValueError("Illegal Command")
        return result


@dataclass
class MaasConfig:
    """
    Provides global information regarding webhook address, passwords etc.

    Plus a list of switch devices. The devices are generic in this module,
    config definitions and function for specific device types are
    in the devices folder.
    """

    name: A[str, desc("The name for this webhook server instance")]
    ip_address: A[str, desc("IP address to listen on")]
    port: A[int, desc("port to listen on")]
    username: A[str, desc("username for connecting to webhook")]
    password: A[str, desc("password for connecting to webhook")]

    devices: A[
        Sequence[SwitchDevice],
        desc("A list of the devices that this webhook server will control"),
    ]

    @classmethod
    def deserialize(cls: Type[T], d: Mapping[str, Any]) -> T:
        return deserialize(cls, d)

    def find_device(self, name: str):
        for device in self.devices:
            if device.name == name:
                return device
        return None
