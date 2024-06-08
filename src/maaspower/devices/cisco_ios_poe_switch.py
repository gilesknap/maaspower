"""
cisco_ios_poe_switch.py
--------------

Classes to represent the configuration and functionality for devices
that can be controlled via Cisco IOS shell commands.
"""

from dataclasses import dataclass
from typing import Annotated as A
from typing import Literal

from netmiko import ConnectHandler

from maaspower.maas_globals import desc
from maaspower.maasconfig import SwitchDevice


@dataclass(kw_only=True)
class CiscoIOSPOESwitch(SwitchDevice):
    """A device controlled via a Cisco IOS PoE switch"""

    name: A[
        str, desc("Logical device name for server connected to the Cisco switch port")
    ]
    ip_address: A[str, desc("IP address of the Cisco IOS PoE switch")]
    username: A[str, desc("Username for the Cisco IOS PoE switch")]
    password: A[str, desc("Password for the Cisco IOS PoE switch")]
    enable_password: A[
        str,
        desc("Enable/secret password for escalating privileges on the Cisco switch"),
    ] = ""
    port_selection_string: A[
        str,
        desc(
            """Port selection for the target device connected to the switch in
            Cisco format"""
        ),
    ]
    port_poe_watts: A[
        int, desc("Power budget (in watts) for the target Cisco switch port")
    ] = -1

    type: Literal["CiscoIOSPOESwitch"] = "CiscoIOSPOESwitch"

    def __post_init__(self):
        """
        Create the 'device' variable, containing properties for establishing \n
        a connection via netmiko.
        """

        super().__post_init__()
        self.device = {
            "device_type": "cisco_ios",
            "host": self.ip_address,
            "username": self.username,
            "password": self.password,
            "secret": self.enable_password,
            "fast_cli": False,
            "allow_auto_change": False,
        }

    def turn_on(self) -> None:
        self._change_power_state(True)

    def turn_off(self) -> None:
        self._change_power_state(False)

    def _change_power_state(self, state: bool):
        """
        Takes a boolean representation of the desired port power state and \n
        affects the desired state on the switch via netmiko.

        Args:
            state: A boolean representation of the power state of the switch port.
        """

        if not state:
            power_cmdline = "power inline never"
        elif state:
            if self.port_poe_watts > 0:
                power_cmdline = f"power inline static max {self.port_poe_watts*1000}"
            else:
                power_cmdline = "power inline auto"
        command_set = [f"interface {self.port_selection_string}", power_cmdline]
        try:
            with ConnectHandler(**self.device) as cisco_conn:
                cisco_conn.enable(check_state=False)
                cisco_conn.send_config_set(command_set)
                cisco_conn.disconnect()
        except Exception as e:
            print(
                f"""Failed to turn device power f{'on' if state else 'off'} for
                port {self.port_selection_string}. Reason: {e}"""
            )
            return "error"

    def query_state(self) -> str:
        """
        Requests the configuration of the desired switch port and parses it to \n
        determine whether the power state is on or off.
        """

        try:
            with ConnectHandler(**self.device) as cisco_conn:
                cisco_conn.enable(check_state=False)
                output = cisco_conn.send_command(
                    f"show running-config interface {self.port_selection_string}"
                )
                cisco_conn.disconnect()
                if "power inline never" in str(output).lower():
                    return "off"
                else:
                    return "on"
        except Exception as e:
            print(f"Failed to query device port state with reason: {e}")
            return "error"
