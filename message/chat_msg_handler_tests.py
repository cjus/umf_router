"""Chat message handler test suite."""

import unittest
from chat_msg_handler import ChatMsgHandler
from umf.umf_message import UMFMessage
from umf.umf_router import UMFRouter
from umf.umf_message import UMFMessageType

__author__ = 'carlosjustiniano'


class ChatMsgHandlerTests(unittest.TestCase):
    """ChatMsgHandlerTests suite. Test that chat message handlers can be
    registered and routed."""

    def test_that_handlers_can_be_registered(self):
        """Assert that handlers can be registered. The result of this test
        should be an increase in the number of handlers for a given type,
        whereby proving successful registration."""
        umf = UMFRouter()
        ChatMsgHandler()
        self.assertTrue(umf.handler_count(UMFMessageType.CHAT) == 1,
                        msg='chat handler registration should have resulted '
                            'in type existing in message_router_map.')

    def test_that_routing_a_registered_message_is_successful(self):
        """Assert that a newly constructed message can be routed."""
        umf = UMFRouter()
        chat = ChatMsgHandler()
        umf.register_handler(UMFMessageType.CHAT, chat.handler)
        msg = {
            "mid": 0,
            "type": "chat",
            "to": "umfTestServer",
            "from": "UMFTester:abcd",
            "version": "1.0",
            "timestamp": "",
            "body": {
            }
        }
        routed = umf.route(None, msg)
        self.assertTrue(routed, msg='msg routing for message of type chat '
                                    'was expected to be routed to a handler.')
