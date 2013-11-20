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
import message
from umf.umf_router import UMFRouter
from umf.umf_message import UMFMessageField


def handle_websocket(ws):
    while True:
        ws_message = ws.receive()
        if ws_message is None:
            print "handle_websocket has ws.received = None, exiting"
            break
        else:
            msg_dict = json.loads(ws_message)
            umf_router = UMFRouter()
            umf_router.route(msg_dict)

            if random.randint(0, 10) > 5:
                t = time.gmtime()
                time_stamp = "%d/%2.2d/%2.2dT%2.2d:%2.2d:%2.2dZ" % \
                             (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                              t.tm_min, t.tm_sec)
                msg = {
                    "mid": uuid4().hex,
                    "type": "chat",
                    "to": msg_dict[UMFMessageField.FROM],
                    "from": "umfTestServer",
                    "version": "1.0",
                    "timestamp": time_stamp,
                    "body": {
                    }
                }
                ws.send(json.dumps(msg))
