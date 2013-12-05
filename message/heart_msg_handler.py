"""HeartMsgHandler
The HeartMsgHandler is a UMF message handler for Heart.
"""
__author__ = 'carlosjustiniano'

from umf.umf_message import UMFMessage
from umf.umf_message import UMFMessageField
from umf.umf_message import UMFMessageType


class HeartBeatMsgHandler(UMFMessage):
    """This is the Heart message handler class. This class is derived from
    UMFMessage which will register this with the UMFRouter."""

    def __init__(self):
        """Get an instance of the UMFRouter and register this handler."""
        UMFMessage.__init__(self, UMFMessageType.HEART, self.handler)

    def handler(self, message, ws):
        """Simply report that the message is being handled, for now.

        Args:
            message: Dictionary with UMF message fields.
            ws: A gevent websocket.

        Returns:
            No return value
        """
        print('HeartMsgHandler handling msg %s from uid %s' %
              (message[UMFMessageField.TYPE], message[UMFMessageField.FROM]))

