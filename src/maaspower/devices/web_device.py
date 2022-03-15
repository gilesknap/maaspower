# Note get the chrome driver for selenium from here:
# https://chromedriver.storage.googleapis.com/index.html?path=100.0.4896.20/

from dataclasses import dataclass
from typing import Optional, cast

from typing_extensions import Literal

from maaspower.maasconfig import MaasConfig, SwitchDevice

from ..webhook import app
from .web_ui import WebGui


@dataclass
class WebDevice(SwitchDevice):
    """Commands for a  device controlled via a Web GUI"""

    type: Literal["WebDevice"] = "WebDevice"

    # this gets called after the dataclass __init__
    def __post_init__(self):
        self.webgui_name = self.name.split("-")[0]
        self.maas_config: Optional[MaasConfig] = None
        self.web_ui: Optional[WebGui] = None

    def validate_command(self, command: str):
        # discover which WebGui we are associated with (name = WebGuiName-CommandName)
        if not self.maas_config:
            self.mass_config = app.config["mass_config"]
            self.web_ui = cast(WebGui, self.mass_config.find_device(self.webgui_name))

        if self.web_ui is not None:
            self.web_ui.execute_command(command)

    def turn_on(self):
        self.validate_command(self.on)

    def turn_off(self):
        self.validate_command(self.off)

    def query_state(self) -> str:
        self.validate_command(self.query)
        return self.web_ui.last_get if self.web_ui else ""
