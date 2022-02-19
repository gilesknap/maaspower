"""
webhook.py
----------
Use Flask to implement a web server that provides web hooks based on
the provided configuration
"""

from flask import Flask
from flask.wrappers import Response
from flask_basicauth import BasicAuth

from .maasconfig import MaasConfig

app = Flask("maaspower")
basic_auth = BasicAuth(app)


@app.route("/")
def hello():
    return "MAAS Power Web Hooks Server"


@app.route("/maaspower/<devicename>/<command>", methods=["POST", "GET"])
@basic_auth.required
def command(devicename: str, command: str):
    """
    Accept webhooks at /maaspower/<devicename>/<command>
    """
    c: MaasConfig = app.config["mass_config"]
    print(f"device: {devicename} command: {command}")
    device = c.find_device(devicename)
    if device is None:
        raise ValueError("unknown device")
    else:
        result = device.do_command(command)

    print(f"response: {result}")
    resp = Response(result)
    return resp


def load_web_hook(c: MaasConfig):
    """
    Setup config for the webserver
    """
    app.config["mass_config"] = c
    app.config["BASIC_AUTH_USERNAME"] = c.username
    app.config["BASIC_AUTH_PASSWORD"] = c.password
    app.config["BASIC_AUTH_FORCE"] = True


def run_web_hook(c: MaasConfig):
    """
    Launch the webserver
    """
    load_web_hook(c)
    app.run(host=c.ip_address, port=c.port)
