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


def send_message(ws, message_fragment):
    """utility function to simplify sending messages"""
    t = time.gmtime()
    time_stamp = "%d/%2.2d/%2.2dT%2.2d:%2.2d:%2.2dZ" % \
                 (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                  t.tm_min, t.tm_sec)
    msg = {
        "mid": uuid4().hex,
        "type": "msg",
        "to": "",
        "from": "umfTestServer",
        "version": "1.0",
        "timestamp": time_stamp,
        "body": {
        }
    }
    # merge message_fragment into msg updating supplied message fields
    msg = dict(msg.items() + message_fragment.items())
    ws.send(json.dumps(msg))


def handle_websocket(ws):
    """Main socket handler"""
    while True:
        ws_message = ws.receive()
        if ws_message is None:
            print "handle_websocket has ws.received = None, exiting"
            break
        else:
            msg_dict = json.loads(ws_message)
            umf_router = UMFRouter()
            routed = umf_router.route(msg_dict)
            if not routed:
                send_message(ws, {
                    "type": "error",
                    "rmid": msg_dict[UMFMessageField.MID],
                    "to": msg_dict[UMFMessageField.FROM],
                    "body": {
                        "errorcode": 400,
                        "message": "unable to route message."
                    }
                })
                # sample code to randomly send a message back to client
            if random.randint(0, 10) > 5:
                send_message(ws, {
                    "type": random.choice(['chat', 'heart',
                                           'mouse', 'client']),
                    "to": msg_dict[UMFMessageField.FROM]
                })
