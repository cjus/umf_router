"""ClientMsgHandler
The ClientMsgHandler is a UMF message handler for Client.
"""
__author__ = 'carlosjustiniano'

from umf.umf_message import UMFMessage
from umf.umf_message import UMFMessageField
from umf.umf_message import UMFMessageType


class ClientMsgHandler(UMFMessage):
    """This is the Client message handler class. This class is derived from
    UMFMessage which will register this with the UMFRouter."""

    def __init__(self):
        """Get an instance of the UMFRouter and register this handler."""
        UMFMessage.__init__(self, UMFMessageType.CLIENT, self.handler)

    def handler(self, ws, message):
        """Simply report that the message is being handled, for now."""
        print('ClientMsgHandler handling msg %s from uid %s' %
              (message[UMFMessageField.TYPE], message[UMFMessageField.FROM]))

