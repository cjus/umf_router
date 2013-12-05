"""UMF Message
The UMF Message base class and helpful enums.
"""
__author__ = 'carlosjustiniano'


class UMFMessageVersion:
    """Definition of supported UMF messaging versions."""
    VERSION_1_0 = '1.0'


class UMFMessageType:
    """Definition of standard UMF message types."""

    CHAT = 'chat'
    CLIENT = 'client'
    ERROR = 'error'
    HEART = 'heart'
    MOUSE = 'mouse'
    MSG = 'msg'


class UMFFormat:
    """Definition of UMF format strings."""
    TIMESTAMP = '%d/%2.2d/%2.2dT%2.2d:%2.2d:%2.2dZ'


class UMFMessageField:
    """Definition of standard UMF message fields."""
    BODY = 'body'
    ERRORCODE = 'errorcode'
    FROM = 'from'
    MESSAGE = 'message'
    MID = 'mid'
    PRIORITY = 'priority'
    RMID = 'rmid'
    TIMESTAMP = 'timestamp'
    TO = 'to'
    TTL = 'ttl'
    TYPE = 'type'
    VERSION = 'version'


class UMFMessage(object):  # pylint: disable=too-few-public-methods
    """UMFMessage base class. All user UMF message handler should derive from
    this class."""

    def __init__(self, msg_type, handler):
        """Self register with UMFRouter.

        Args:
            message_type: UMFMessageType field
            handler: function handler to register
        """
        from umf_router import UMFRouter

        umf_router = UMFRouter()
        umf_router.register_handler(msg_type, handler)

    def handler(self, message, ws):
        """Base handler fires exception when derived class doesn't include
        its own handler.

        Args:
            message: Dictionary with UMF message fields.
            ws: A gevent websocket.
        """
        raise Exception('UMFMessage derived class must implement its own '
                        'handler.')
