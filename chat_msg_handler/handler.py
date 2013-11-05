# coding: utf-8

from umf.umf_router import UMFRouter


class ChatMsgHandler:
    def __init__(self):
        print "ChatMsgHandler init"
        umf_router = UMFRouter()
        umf_router.register_handler("chat", self.handler)

    def handler(self, message):
        print "ChatMsgHandler handling msg %s from uid %s" % (message["type"], message["from"])

