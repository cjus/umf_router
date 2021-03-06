#!/usr/bin/env python
"""Init WSGIServer and websocket_handler"""
__author__ = 'carlosjustiniano'

from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app import websocket_handler

if __name__ == '__main__':
    monkey.patch_all()
    WEB_SOCKET_PORT = 80
    print('Starting WebSocket server on http://0.0.0.0:%s' % WEB_SOCKET_PORT)
    http_server = WSGIServer(('', WEB_SOCKET_PORT), websocket_handler,
                             handler_class=WebSocketHandler)
    http_server.serve_forever()
