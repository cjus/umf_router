"""UMF Message
The UMF Message base class and helpful enums.
"""
__author__ = 'carlosjustiniano'


class UMFMessageType:
    """Definition of standard UMF message types."""

    CHAT = 'chat'
    CLIENT = 'client'
    HEART = 'heart'
    MOUSE = 'mouse'


class UMFMessageField:
    """Definition of standard UMF message fields."""

    FROM = 'from'
    TO = 'to'
    TYPE = 'type'
    MID = 'mid'
    RMID = 'rmid'


class UMFMessage:
    """UMFMessage base class. All user UMF message handler should derive from
    this class."""

    def __init__(self, msg_type, handler):
        """Self register with UMFRouter."""
        from umf_router import UMFRouter

        umf_router = UMFRouter()
        umf_router.register_handler(msg_type, handler)

    def handler(self, ws, message):
        """Base handler fires exception when derived class doesn't include
        its own handler."""
        raise Exception("UMFMessage derived class must implement its own "
                        "handler.")
