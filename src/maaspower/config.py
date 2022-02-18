"""
The MaasConfig class is an in memory representation of the contents of
the maaspower YAML configuration file that specifies the set of power
manager devices for which to serve web hooks.

This module uses APISchema to serialize and deserialize the config
file, plus provide a schema for the the config.
"""

from dataclasses import dataclass
from typing import Any, Mapping, Sequence, Type

from apischema import deserialize
from typing_extensions import Annotated as A

from .globals import T, desc


@dataclass
class Devices:
    """
    A base class for the devices that the webhook server will control
    concrete subclasses are found in the devices subfolder
    """


@dataclass
class MaasConfig:
    """
    Provides global information regarding webhook root URLs, passwords etc.

    Plus a list of devices. The devices are generic in this module,
    config definitions and function for specific device types are
    in the devices folder
    """

    name: A[str, desc("The name for this webhook server instance")]
    rooturi: A[str, desc("The root URI for all webhooks served")]
    ip_address: A[str, desc("IP address to listen on")]
    port: A[int, desc("port to listen on")]
    username: A[str, desc("username for connecting to webhook")]
    password: A[str, desc("password for connecting to webhook")]

    devices: A[
        Sequence[Devices],
        desc("A list of the devices that this webhook server will control"),
    ]

    @classmethod
    def deserialize(cls: Type[T], d: Mapping[str, Any]) -> T:
        return deserialize(cls, d)
