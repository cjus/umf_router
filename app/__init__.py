# coding: utf-8
import os

from flask import Flask
from websocket import handle_websocket

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.urandom(24)
app.debug = True

def websocket_handler(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/":
        return app(environ, start_response)
    elif path == "/ws":
        handle_websocket(environ["wsgi.websocket"])
    else:
        return app(environ, start_response)


import views
