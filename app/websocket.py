"""websocket handler
Loads the UMFRouter and registers our sample message handlers.
Also sets up the handling of each websocket and passes messages onto the
umf_router as they're received.
"""
__author__ = 'carlosjustiniano'

import json
import random
import time
from uuid import uuid4
from umf.umf_router import UMFRouter
from chat_msg_handler.handler import ChatMsgHandler
from heart_msg_handler.handler import HeartBeatMsgHandler
from client_msg_handler.handler import ClientMsgHandler
from mouse_msg_handler.handler import MouseMsgHandler

umf_router = UMFRouter()

# instanciate UMF message handlers
chat_msg_handler = ChatMsgHandler()
heart_msg_handler = HeartBeatMsgHandler()
mouse_msg_handler = MouseMsgHandler()
client_msg_handler = ClientMsgHandler()


def handle_websocket(ws):
    while True:
        message = ws.receive()
        if message is None:
            print "handle_websocket has ws.received = None, exiting"
            break
        else:
            message = json.loads(message)
            umf_router.route(message)

            if random.randint(0, 10) > 5:
                t = time.gmtime()
                time_stamp = "%d/%2.2d/%2.2dT%2.2d:%2.2d:%2.2dZ" % \
                             (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
                msg = {
                    "mid": uuid4().hex,
                    "type": "chat",
                    "to": message["from"],
                    "from": "umfTestServer",
                    "version": "1.0",
                    "timestamp": time_stamp,
                    "body": {
                    }
                }
                ws.send(json.dumps(msg))
