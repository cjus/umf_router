#!/usr/bin/env python
"""Init WSGIServer and websocket_handler"""
__author__ = 'carlosjustiniano'

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app import websocket_handler

if __name__ == '__main__':
    WEB_SOCKET_PORT = 5000
    http_server = WSGIServer(('', WEB_SOCKET_PORT), websocket_handler, handler_class=WebSocketHandler)
    http_server.serve_forever()
