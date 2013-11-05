# coding: utf-8

from umf.umf_router import UMFRouter


class HeartBeatMsgHandler:
    def __init__(self):
        print "HeartBeatMsgHandler init"
        umf_router = UMFRouter()
        umf_router.register_handler("heart", self.handler)

    def handler(self, message):
        print "HeartBeatMsgHandler handling msg %s from uid %s" % (message["type"], message["from"])
