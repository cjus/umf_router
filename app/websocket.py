# coding: utf-8
import json
from umf.umf_router import UMFRouter

from chat_msg_handler.handler import ChatMsgHandler
from heart_msg_handler.handler import HeartBeatMsgHandler

umf_router = UMFRouter()

# instanciate UMF message handlers
chat_msg_handler = ChatMsgHandler()
heart_msg_handler = HeartBeatMsgHandler()


def handle_websocket(ws):
    while True:
        message = ws.receive()
        if message is None:
            print "handle_websocket as ws.received = None, exiting"
            break
        else:
            message = json.loads(message)
            umf_router.route(message)

            #r = "I have received this message from you : %s" % message
            #r += "<br>Glad to be your webserver."
            #ws.send(json.dumps({'output': r}))
