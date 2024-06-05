# Note get the chrome driver for selenium from here:
# https://chromedriver.storage.googleapis.com/index.html?path=100.0.4896.20/

import re
from dataclasses import dataclass
from enum import Enum
from time import sleep
from typing import Annotated as A
from typing import Literal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from maaspower.maas_globals import desc
from maaspower.maasconfig import RegexSwitchDevice

command_regex = re.compile(r"([^\/]*)\/([^\/]*)\/?([^\/]*)?\/?([^\/]*)?$")
index_regex = re.compile(r"(.*)\[([0-9]*)\]")


class FindBy(Enum):
    id = By.ID
    cls = By.CLASS_NAME
    link = By.PARTIAL_LINK_TEXT
    n = By.NAME
    css = By.CSS_SELECTOR


@dataclass(kw_only=True)
class WebGui(RegexSwitchDevice):
    """A device controlled via a Web GUI"""

    type: Literal["WebGui"] = "WebGui"

    connect_url: A[str, desc("URL to Web UI")] = "none"
    login: A[str, desc("command sequence to log in")] = "none"
    logout: A[str, desc("command sequence to log out")] = "none"
    timeout: A[int, desc("max timeout on any UI transitions")] = 10
    driver: A[str, desc("Path to chromedriver binary")] = "./chromedriver"

    # this gets called after the dataclass __init__
    def __post_init__(self):
        self.last_get = ""
        self.connect()

    def __del__(self):
        self.disconnect()

    def connect(self, retries=2):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.c_driver = webdriver.Chrome(self.driver, options=options)

        self.c_driver.get(self.connect_url)
        self.c_driver.timeouts._implicit_wait = self.timeout

        self.execute_command(self.login, retries=retries)

    def disconnect(self):
        self.execute_command(self.logout, retries=0)
        try:
            self.c_driver.close()
        except Exception:
            pass

    def execute_command(self, command_list: str, retries=2):
        """
        Take a sequence of command strings separated by \n.
        Each command identifies and interacts with an HTML element
        """

        element_list = command_list.split("\n")[:-1]
        for element in element_list:
            # separate out the elements of the string
            match = command_regex.match(element)
            if match is None:
                raise ValueError(f"bad command format: {element} {element_list}")

            command = match.group(1)

            while retries >= 0:
                try:
                    # invoke the command via selenium
                    if command == "click":
                        self.click(match.group(2), match.group(3))
                    elif command == "send":
                        self.send(match.group(2), match.group(3), match.group(4))
                    elif command == "sendcr":
                        self.send(
                            match.group(2), match.group(3), match.group(4), cr=True
                        )
                    elif command == "get":
                        self.last_get = self.get(match.group(2), match.group(3))
                    elif command == "delay":
                        sleep(float(match.group(2)))
                except Exception:
                    retries -= 1
                    if retries > 0:
                        self.disconnect()
                        self.connect(retries=0)
                else:
                    # success - leave the retry loop
                    break
            else:
                # abort remaining commands when failed retry times
                return

    def process_arguments(self, by_str: str, value: str) -> tuple[str, str, int | None]:
        # convert our short fieldtype string to the full selenium string
        by = FindBy[by_str].value

        # check for and index [n] at the end of a string. Used for
        # matching > 1 html element and we want to index into the list of matches
        idx_match = index_regex.match(value)
        if idx_match is None:
            index = None
        else:
            value = idx_match.group(1)
            index = int(idx_match.group(2))
        return by, value, index

    def click(self, by_str: str, value: str):
        by, value, index = self.process_arguments(by_str, value)
        elem = WebDriverWait(self.c_driver, self.timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        if index is not None:
            elements = self.c_driver.find_elements(by=by, value=value)
            elem = elements[index]
        elem.click()

    def send(self, by_str: str, value: str, text: str, cr=False):
        by, value, index = self.process_arguments(by_str, value)
        if cr:
            text += "\n"
        elem = WebDriverWait(self.c_driver, self.timeout).until(
            EC.presence_of_element_located((by, value))
        )
        if index:
            elements = self.c_driver.find_elements(by=by, value=value)
            elem = elements[index]
        elem.send_keys(text)

    def get(self, by_str: str, value) -> str:
        by, value, index = self.process_arguments(by_str, value)
        elem = WebDriverWait(self.c_driver, self.timeout).until(
            EC.presence_of_element_located((by, value))
        )
        if index:
            elements = self.c_driver.find_elements(by=by, value=value)
            elem = elements[index]
        return elem.text
