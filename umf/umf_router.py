"""UMF_Router
The UMFRouter uses the singleton design pattern to function as the single
message router for our application.
"""
__author__ = 'carlosjustiniano'

import json
import time

from uuid import uuid4
from umf.umf_message import UMFMessageField
from umf.umf_message import UMFMessageVersion
from umf.umf_message import UMFMessageType
from umf.umf_message import UMFFormat


def singleton(cls):  # pylint: disable=too-few-public-methods
    """This is a singleton helper function."""

    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


@singleton
class UMFRouter(object):  # pylint: disable=too-few-public-methods
    """UMFRouter singleton class. Helpful in ensuring that only one instance
    of this class is available to the entire system.
    """

    def __init__(self):
        """Init message router dictionary."""
        self.message_router_map = {}

    def type_exists(self, message_type):
        """Test if type is already registered and in message_router_map.

        Args:
            message_type: A supported UMFMessageType type const.

        Returns:
            A Boolean value, True if found, False if not found.
        """
        return message_type in self.message_router_map

    def handler_count(self, message_type):
        """Return count of handler for a message_type.

        Args:
            message_type: A supported UMFMessageType type const.

        Returns:
            A count of handlers for a given message_type.
        """
        if self.type_exists(message_type):
            return len(self.message_router_map[message_type])
        return 0

    def register_handler(self, message_type, handler):
        """Register a handler for a specific message_type.

        Args:
            message_type: A supported UMFMessageType type const.
            handler: A reference to a function handler.

        Returns:
            Boolean True
        """
        if not self.type_exists(message_type):
            self.message_router_map[message_type] = []
        self.message_router_map[message_type].append(handler)
        print('    Handler registered for %s by %s' % (message_type, handler))
        return True

    def route(self, message, ws):
        """Route a message to one or more registered handlers.

        Args:
            message_type: A supported UMFMessageType type const.
            ws: A gevent websocket.

        Returns:
            Boolean True if routed, else False
        """
        if message[UMFMessageField.TYPE] not in self.message_router_map:
            print('message %s not in message_router_map' %
                  message[UMFMessageField.TYPE])
            if ws:
                msg = {
                    UMFMessageField.TYPE: UMFMessageType.ERROR,
                    UMFMessageField.RMID: message[UMFMessageField.MID],
                    UMFMessageField.TO: message[UMFMessageField.FROM],
                    UMFMessageField.BODY: {
                        'errorcode': 400,
                        'message': "unable to route message."
                    }
                }
                self.send_message(msg, ws)
            return False

        for handler in self.message_router_map[message[UMFMessageField.TYPE]]:
            handler(message, ws)
        return True

    def send_message(self, message_fragment, ws=None):
        """Utility function to simplify sending messages.

        Args:
            message_fragment: Dictionary with UMF message field overrides.
            ws: A gevent websocket.

        Returns:
            No return value
        """
        if ws is None:
            return
        t = time.gmtime()
        time_stamp = UMFFormat.TIMESTAMP % \
                     (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                      t.tm_min, t.tm_sec)
        msg = {
            UMFMessageField.MID: uuid4().hex,
            UMFMessageField.TYPE: UMFMessageType.MSG,
            UMFMessageField.TO: '',
            UMFMessageField.FROM: 'umfTestServer',
            UMFMessageField.VERSION: UMFMessageVersion.VERSION_1_0,
            UMFMessageField.TIMESTAMP: time_stamp,
            UMFMessageField.BODY: {
            }
        }
        # merge message_fragment into msg updating supplied message fields
        msg = dict(msg.items() + message_fragment.items())
        ws.send(json.dumps(msg))
