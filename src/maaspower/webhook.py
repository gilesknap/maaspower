from typing import Dict

from flask import Flask, request

app = Flask("maaspower")


@app.route("/")
def hello():
    return "Webhooks with Python"


@app.route("/test", methods=["POST"])
def my_test():
    if request.authorization is not None:
        auth: Dict = request.authorization
        user = auth.get("username")
        password = auth.get("password")
        print(f"Test user {user}, pass {password}")
    return "OK"


def run_web_hook():
    app.run(host="0.0.0.0", port=5000)
