# Note get the chrome driver for selenium from here:
# https://chromedriver.storage.googleapis.com/index.html?path=100.0.4896.20/

import os
import re
from enum import Enum
from pathlib import Path
from time import sleep
from typing import List, Optional, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

this_dir = Path(__file__).parent
os.chdir(this_dir)

driver = webdriver.Chrome("./chromedriver")

url = "http://192.168.0.137/index.cgi"

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


def process_arguments(by_str: str, value: str) -> Tuple[str, str, Optional[int]]:
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


def sequence(elements: List[str]):
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
    for idx, element in enumerate(elements):
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


login = ["send/cls/pwd-field-text/Piggy00n\n", "click/link/POE"]


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


sequence(login)
sequence(disable)
# sequence(logout)
