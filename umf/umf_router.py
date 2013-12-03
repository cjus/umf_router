"""UMF_Router
The UMFRouter uses the singleton design pattern to function as the single
message router for our application.
"""
__author__ = 'carlosjustiniano'

import json
import time

from uuid import uuid4
from umf_message import UMFMessageField


def singleton(cls):
    """This is a singleton helper function."""

    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


@singleton
class UMFRouter:
    """UMFRouter singleton class. Helpful in ensuring that only one instance
    of this class is available to the entire system.
    """

    def __init__(self):
        """Init message router dictionary."""
        self.message_router_map = {}

    def type_exists(self, message_type):
        """Test if type is already registered and in message_router_map."""
        return message_type in self.message_router_map

    def handler_count(self, message_type):
        """Return count of handler for a message_type."""
        if self.type_exists(message_type):
            return len(self.message_router_map[message_type])
        return 0

    def register_handler(self, message_type, handler):
        """Register a handler for a specific message_type."""
        if not self.type_exists(message_type):
            self.message_router_map[message_type] = []
        self.message_router_map[message_type].append(handler)
        print('    Handler registered for %s by %s' % (message_type, handler))
        return True

    def route(self, message, ws):
        """Route a message to one or more registered handlers."""
        routed = True
        if message[UMFMessageField.TYPE] not in self.message_router_map:
            print('message %s not in message_router_map' %
                  message[UMFMessageField.TYPE])
            if ws:
                self.send_message({
                                      "type": "error",
                    "rmid": message[UMFMessageField.MID],
                    "to": message[UMFMessageField.FROM],
                    "body": {
                        "errorcode": 400,
                        "message": "unable to route message."
                    }
                                  }, ws)
            return False

        for handler in self.message_router_map[message[UMFMessageField.TYPE]]:
            handler(message, ws)
        return routed

    def send_message(self, message_fragment, ws=None):
        """utility function to simplify sending messages"""
        if ws is None:
            return
        t = time.gmtime()
        time_stamp = "%d/%2.2d/%2.2dT%2.2d:%2.2d:%2.2dZ" % \
                     (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                      t.tm_min, t.tm_sec)
        msg = {
            "mid": uuid4().hex,
            "type": "msg",
            "to": "",
            "from": "umfTestServer",
            "version": "1.0",
            "timestamp": time_stamp,
            "body": {
            }
        }
        # merge message_fragment into msg updating supplied message fields
        msg = dict(msg.items() + message_fragment.items())
        ws.send(json.dumps(msg))
