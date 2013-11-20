"""MouseMsgHandler
The MouseMsgHandler is a UMF message handler for mouse.
"""
__author__ = 'carlosjustiniano'

from umf.umf_message import UMFMessage
from umf.umf_message import UMFMessageField
from umf.umf_message import UMFMessageType


class MouseMsgHandler(UMFMessage):
    """This is the mouse message handler class. This class is derived from
    UMFMessage which will register this with the UMFRouter."""

    def __init__(self):
        """Get an instance of the UMFRouter and register this handler."""
        UMFMessage.__init__(self, UMFMessageType.MOUSE, self.handler)

    def handler(self, message):
        """Simply report that the message is being handled, for now."""
        print('MouseMsgHandler handling msg %s from uid %s' %
              (message[UMFMessageField.TYPE], message[UMFMessageField.FROM]))

