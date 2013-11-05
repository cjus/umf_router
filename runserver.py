#!/usr/bin/env python
"""Init WSGIServer and websocket_handler"""
__author__ = 'carlosjustiniano'

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app import websocket_handler

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), websocket_handler, handler_class=WebSocketHandler)
    http_server.serve_forever()
