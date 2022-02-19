"""
shell_cmd.py
------------

Classes to represent the configuration and functionality for devices
that can be controlled via a command line utility.

e.g. smart power switching usb hubs https://github.com/mvp/uhubctl
"""
import subprocess
from dataclasses import dataclass

from typing_extensions import Literal

from maaspower.maasconfig import SwitchDevice


@dataclass
class CommandLine(SwitchDevice):
    """A device controlled via a command line utility"""

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

    def query_state(self) -> str:
        return self.execute_command(self.query)
