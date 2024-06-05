"""
shell_cmd.py
------------

Classes to represent the configuration and functionality for devices
that can be controlled via a command line utility.

e.g. smart power switching usb hubs https://github.com/mvp/uhubctl
"""

import subprocess
from dataclasses import dataclass
from typing import Annotated as A
from typing import Literal

from maaspower.maas_globals import desc
from maaspower.maasconfig import RegexSwitchDevice


@dataclass(kw_only=True)
class CommandLine(RegexSwitchDevice):
    """A device controlled via a command line utility"""

    on: A[str, desc("command line string to switch device on")]
    off: A[str, desc("command line string to switch device off")]
    query: A[str, desc("command line string to query device state")]
    query_on_regex: A[str, desc("match the on status return from query")] = "on"
    query_off_regex: A[str, desc("match the off status return from query")] = "off"

    type: Literal["CommandLine"] = "CommandLine"

    def execute_command(self, command: str):
        print(f"EXECUTE command line: {command}")
        params = command.split(" ")
        process = subprocess.Popen(
            params, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        print(stdout.decode(), stderr.decode())

        return stdout.decode()

    def turn_on(self):
        self.execute_command(self.on)

    def turn_off(self):
        self.execute_command(self.off)

    def run_query(self) -> str:
        return self.execute_command(self.query)
