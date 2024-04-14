# Web UI playground.
#
# To work out the sequence of elements you need to interact with to
# Web scrape the power control and query from your device use this module
# with ipython (replace URL with your device)
#
#    activate your venv
#    pip install ipython
#    ipython webtestui.py -i http://192.168.0.137/index.cgi
#
# This will run the code below and drop you into a prompt and pop up a Chrome
# window
# Now you can use the (right-click ) inspect in chrome to take a look at
# which HTML elements you need to poke to login, and control PoE ports.
# You will need to find a unique property of the element to identify
# it. This code supports classname, name, partial link text and ID. See
# class FindBy for details
#
# take a look at the example sequences login/enable/disable/logout and
# develop your own for your device. These can then be added to the config
# file for your maaspower setup.

# You need Chrome or Chromium installed for this to work
# Also you need to download the ChromeDriver
#
# Get the chrome driver for selenium from here (pick one that matches
# your Chrome version):
# https://chromedriver.storage.googleapis.com/index.html
# and place it in the same folder as this file

import os
import re
import sys
from enum import Enum
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

this_dir = Path(__file__).parent
os.chdir(this_dir)

driver = webdriver.Chrome("./chromedriver")

url = sys.argv[1]

driver.get(url)
driver.timeouts._implicit_wait = 20

command_regex = re.compile(r"([^\/]*)\/([^\/]*)\/?([^\/]*)?\/?([^\/]*)?$")
index_regex = re.compile(r"(.*)\[([0-9]*)\]")


class FindBy(Enum):
    id = By.ID
    cls = By.CLASS_NAME
    link = By.PARTIAL_LINK_TEXT
    n = By.NAME
    css = By.CSS_SELECTOR


def process_arguments(by_str: str, value: str) -> tuple[str, str, int | None]:
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


def click(by_str: str, value: str):
    by, value, index = process_arguments(by_str, value)
    print(f"click on {by} {value} with index {index}")
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value)))
    if index is not None:
        elements = driver.find_elements(by=by, value=value)
        elem = elements[index]
    elem.click()


def send(by_str: str, value: str, text: str):
    by, value, index = process_arguments(by_str, value)
    print(f"send {text} to {by} {value} with index {index}")
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
    if index:
        elements = driver.find_elements(by=by, value=value)
        elem = elements[index]
    elem.send_keys(text)


def get(by_str: str, value) -> str:
    by, value, index = process_arguments(by_str, value)
    print(f"get field {by} {value} with index {index}")
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
    if index:
        elements = driver.find_elements(by=by, value=value)
        elem = elements[index]
    return elem.text


def sequence(elements: list[str]):
    """
    take a sequence of strings of the form
    command_by_value
    where:
      command is click or send
      by is one of id, classname, link, named
      value is the value for the id, class, partial link text, name of the
        html element to interact with
    when the command is 'send' the next string in the sequence is the text to
    send to the html element
    """
    for element in elements:
        # separate out the elements of the string
        match = command_regex.match(element)
        if match is None:
            raise (ValueError(f"bad command format: {element}"))

        command = match.group(1)

        # invoke the command via selenium
        if command == "click":
            click(match.group(2), match.group(3))
        elif command == "send":
            send(match.group(2), match.group(3), match.group(4))
        elif command == "get":
            click(match.group(2), match.group(3))
        elif command == "delay":
            sleep(float(match.group(2)))


# these example sequences work for the Netgear G308EP

login = ["send/cls/pwd-field-text/MYPASSWORD\n", "click/link/POE"]

# Control PoE port 3 of 8
disable = [
    "click/n/isShowPot3",
    "click/n/editPot3",
    "click/cls/poePortPwrTxt",
    "click/link/Disable",
    "click/n/submitPotedit",
]

enable = [
    "click/n/isShowPot3",
    "click/n/editPot3",
    "click/cls/poePortPwrTxt",
    "click/link/Enable",
    "click/n/submitPotedit",
]

logout = [
    "click/cls/src-views-header-nav-icon-button",
    "click/cls/icon-logout",
    "click/id/modal_footer_button_primary",
]


# sequence(login)
# sequence(disable)
# sequence(logout)
