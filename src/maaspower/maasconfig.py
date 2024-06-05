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
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass, fields
from typing import Annotated as A
from typing import Any, ClassVar

from apischema import deserialize, identity
from apischema.conversions import Conversion, deserializer
from typing_extensions import override

from .maas_globals import MaasResponse, T, desc


@dataclass(kw_only=True)
class SwitchDevice(ABC):
    """
    A base class for the switching devices that the webhook server will control.

    Concrete subclasses MUST provide a `type` field akin to this:

    type: Literal["ConreteDevice"] = "ConcreteDevice"

    Concrete subclasses are found in the devices subfolder
    """

    name: A[str, desc("A name for the switching device")]

    # command functions to be implemented in the derived classes
    @abstractmethod
    def turn_on(self) -> None: ...

    @abstractmethod
    def turn_off(self) -> None: ...

    @abstractmethod
    def query_state(self) -> str: ...

    def __post_init__(self):
        # allow regular expressions for names but if the name is an
        # illegal expression then just use it as a simple string match
        try:
            self._name_regx = re.compile(self.name)
        except re.error:
            self._name_regx = None

    # https://wyfo.github.io/apischema/examples/subclass_union/
    def __init_subclass__(cls):
        # Deserializers stack directly as a Union
        deserializer(Conversion(identity, source=cls, target=SwitchDevice))

    def copy(self, new_name: str, match) -> "SwitchDevice":
        """
        Create a copy of this device with a new name.
        All the fields of the object are reformatted with substitutions in
        regex matches using {name} for the whole match and {m1} {m2} etc
        for matching subgroups.

        This is used for creating a specific instance of a device from
        a regex defined device.
        """
        result = deepcopy(self)

        # TODO can't find an easy way to iterate over dataclass field instances
        for field in fields(self):
            if field.name == "name":
                continue
            setattr(result, field.name, match.expand(getattr(result, field.name)))

        result.name = new_name

        return result

    def do_command(self, command) -> str | None:
        result = None

        if command == "on":
            self.turn_on()
        elif command == "off":
            self.turn_off()
        elif command == "query":
            return self.query_state()
        else:
            raise ValueError("Illegal Command")
        return result


@dataclass(kw_only=True)
class RegexSwitchDevice(SwitchDevice, ABC):
    """
    An abstract `SwitchDevice` which has the ability to interpret reponses
    and convert them to the requisit MaasReponse values using regex.

    """

    query_on_regex: A[str, desc("match the on status return from query")] = "on"
    query_off_regex: A[str, desc("match the off status return from query")] = "off"

    @abstractmethod
    def run_query(self) -> str:
        """
        Ths method should be overridden by concrete classes. This method
        is called by query_state and it's response is run through query_regex_on
        and query_regex_off.

        returns: A value to be parsed by query_regex_on and query_regex_off.
        """
        ...

    @override
    def query_state(self) -> str:
        """
        Uses the regex patterns defined in query_on_regex and query_off_regex
        to ascertain the correct response.
        """
        query_response = self.run_query()
        if re.search(self.query_on_regex, query_response, flags=re.MULTILINE):
            return MaasResponse.on.value
        elif re.search(self.query_off_regex, query_response, flags=re.MULTILINE):
            return MaasResponse.off.value
        else:
            raise ValueError(
                f"Unknown power state response: \n{query_response}\n"
                f"\nfor regexes {self.query_on_regex}, {self.query_off_regex}"
            )


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

    # this is a classvar to stop it appearing in the schema
    _devices: ClassVar[dict[str, SwitchDevice]] = {}

    @classmethod
    def deserialize(cls: type[T], d: Mapping[str, Any]) -> T:
        config: Any = deserialize(cls, d)
        # create indexed list of devices
        config._devices = {device.name: device for device in config.devices}
        return config

    def find_device(self, name: str):
        """
        use the indexed list to find the device or walk through the and check
        for regex matches.
        A regex match creates a new device which goes in the _devices cache
        so will not need matching a second time

        TODO https://github.com/gilesknap/maaspower/issues/10#issue-1222292918
        """
        if name in self._devices:
            return self._devices[name]
        for device in self.devices:
            if device._name_regx:
                match = device._name_regx.match(name)
                if match:
                    # create a copy with the correct name and substituted commands
                    # and cache it
                    self._devices[name] = device.copy(name, match)
                    return self._devices[name]
        return None
