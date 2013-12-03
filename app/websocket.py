"""websocket handler
Loads the UMFRouter and registers our sample message handlers.
Also sets up the handling of each websocket and passes messages onto the
umf_router as they're received.
"""
__author__ = 'carlosjustiniano'

import json
import random
import message

from umf.umf_router import UMFRouter
from umf.umf_message import UMFMessageField


def handle_websocket(ws):
    """Main socket handler"""
    while True:
        ws_message = ws.receive()
        if ws_message is None:
            print "handle_websocket has ws.received = None, exiting"
            break
        else:
            msg_dict = json.loads(ws_message)
            print('received message: %s' % msg_dict)
            umf_router = UMFRouter()
            umf_router.route(msg_dict, ws)

            # sample code to randomly send a message back to client
            if random.randint(0, 10) > 5:
                umf_router.send_message({
                                            "type": random.choice(['chat', 'heart',
                                           'mouse', 'client']),
                    "to": msg_dict[UMFMessageField.FROM]
                                        }, ws)
