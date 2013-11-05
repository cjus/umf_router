"""ChatMsgHandler
The ChatMsgHandler is a UMF message handler for chat.
"""
__author__ = 'carlosjustiniano'

from umf.umf_router import UMFRouter


class ChatMsgHandler:
    def __init__(self):
        """get an instance of the UMFRouter and register this handler"""
        print "ChatMsgHandler init"
        umf_router = UMFRouter()
        umf_router.register_handler("chat", self.handler)

    def handler(self, message):
        """simply report that the message is being handled, for now"""
        print "ChatMsgHandler handling msg %s from uid %s" % (message["type"], message["from"])

