"""
devices package
===============

Each SwitchDevice derived class in this package adds support for a type
of switching device.
"""

from . import shell_cmd, smart_thing, web_device, web_ui

# __all__ defines the public API for the package.
# Each module also defines its own __all__.
__all__ = ["shell_cmd", "smart_thing", "web_ui", "web_device", "cisco_ios_poe_switch"]
