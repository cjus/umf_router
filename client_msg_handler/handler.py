"""ClientMsgHandler
The ClientMsgHandler is a UMF message handler for client.
"""
__author__ = 'carlosjustiniano'

from umf.umf_router import UMFRouter


class ClientMsgHandler:
    def __init__(self):
        """get an instance of the UMFRouter and register this handler"""
        print "ClientMsgHandler init"
        umf_router = UMFRouter()
        umf_router.register_handler("client", self.handler)

    def handler(self, message):
        """simply report that the message is being handled, for now"""
        print "ClientMsgHandler handling msg %s from uid %s" % (message["type"], message["from"])

