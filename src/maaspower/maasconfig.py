"""
The MaasConfig class is an in memory representation of the contents of
the maaspower YAML configuration file that specifies the set of power
manager devices for which to serve web hooks.

This module uses APISchema to serialize and deserialize the config
file, plus provide a schema for the the config.
"""

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Type

from apischema import deserialize
from apischema.conversions import Conversion, deserializer, identity
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
    query: A[str, desc("command line string to query device state")] = "none"

    description: A[Optional[str], desc("A description of the device's purpose")] = ""

    type: str = "none"  # a literal to distinguish the subclasses of Device

    # https://wyfo.github.io/apischema/examples/subclass_union/
    def __init_subclass__(cls):
        # Deserializers stack directly as a Union
        deserializer(Conversion(identity, source=cls, target=SwitchDevice))

    # command functions to be implemented in the derived classes
    def turn_on(self) -> MaasResponse:
        raise (NotImplementedError)

    def turn_off(self) -> MaasResponse:
        raise (NotImplementedError)

    def query_state(self) -> MaasResponse:
        raise (NotImplementedError)

    def do_command(self, command):
        if command == "on":
            res = self.turn_on()
        elif command == "off":
            res = self.turn_off()
        elif command == "query":
            res = self.query_state()
        else:
            raise ValueError("Illegal Command")
        return res.value


@dataclass
class MaasConfig:
    """
    Provides global information regarding webhook root URLs, passwords etc.

    Plus a list of devices. The devices are generic in this module,
    config definitions and function for specific device types are
    in the devices folder
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
