"""
cisco_ios_poe_switch.py
--------------

Classes to represent the configuration and functionality for devices
that can be controlled via Cisco IOS shell commands.

"""

from dataclasses import dataclass
from threading import Lock, Thread

from netmiko import ConnectHandler
from typing_extensions import Annotated as A
from typing_extensions import Literal

from maaspower.maas_globals import desc
from maaspower.maasconfig import SwitchDevice


@dataclass(kw_only=True)
class CiscoIOSPOESwitch(SwitchDevice):
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
        super().__post_init__()
        self.mutex = Lock()
        self.device = {
            "device_type": "cisco_ios",
            "host": self.ip_address,
            "username": self.username,
            "password": self.password,
            "secret": self.enable_password,
        }

    def turn_on(self) -> None:
        thread = Thread(target=self._change_power_state, kwargs={"state": True})
        thread.start()

    def turn_off(self) -> None:
        thread = Thread(target=self._change_power_state, kwargs={"state": False})
        thread.start()

    def _change_power_state(self, state: bool):
        with self.mutex:
            if not state:
                power_cmdline = "power inline never"
            elif state:
                if self.port_poe_watts > 0:
                    power_cmdline = (
                        f"power inline static max {self.port_poe_watts*1000}"
                    )
                else:
                    power_cmdline = "power inline auto"
            command_set = [
                ["conf t", ""],
                [f"interface {self.port_selection_string}", ""],
                [power_cmdline, ""],
            ]
            try:
                with ConnectHandler(**self.device) as cisco_conn:
                    cisco_conn.enable()
                    for cmd in command_set:
                        cisco_conn.send_command(
                            command_string=cmd[0],
                            expect_string=cmd[1],
                            cmd_verify=False,
                        )
                    cisco_conn.disconnect()
            except Exception as e:
                print(
                    f"""Failed to turn device power f{'on' if state else 'off'} for
                    port {self.port_selection_string}. Reason: {e}"""
                )
                return "error"

    def query_state(self) -> str:
        try:
            with ConnectHandler(**self.device) as cisco_conn:
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
