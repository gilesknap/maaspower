"""
webhook.py
----------
Use Flask to implement a web server that provides web hooks based on
the provided configuration
"""

from typing import Dict

from flask import Flask, request
from flask.wrappers import Response

from .maasconfig import MaasConfig

app = Flask("maaspower")


@app.route("/")
def hello():
    return "MAAS Power Web Hooks Server"


@app.route("/maaspower/<devicename>/<command>", methods=["POST", "GET"])
def command(devicename: str, command: str):
    """
    Accept webhooks at /maaspower/<devicename>/<command>
    """
    c: MaasConfig = app.config["mass_config"]
    print(f"device: {devicename} command: {command}")
    if request.authorization is not None:
        auth: Dict = request.authorization
        if auth.get("username") != c.username or auth.get("password") != c.password:
            raise (ValueError("bad credentials"))
        device = c.find_device(devicename)
        if device is None:
            raise ValueError("unknown device")
        else:
            result = device.do_command(command)
    else:
        raise (ValueError("no credentials"))
    print(f"response: {result}")
    resp = Response(result)
    return resp


def run_web_hook(c: MaasConfig):
    """
    Launch the webserver
    """
    app.config["mass_config"] = c
    app.run(host=c.ip_address, port=c.port)
