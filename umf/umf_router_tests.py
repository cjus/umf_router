"""umf_router test suite.
"""
import unittest
from umf.umf_message import UMFMessage
from umf.umf_message import UMFMessageField
from umf.umf_message import UMFMessageType
from umf.umf_message import UMFMessageVersion
from umf.umf_router import UMFRouter

__author__ = 'carlosjustiniano'


class BadHandler(UMFMessage):
    """This is a bad UMF handler because it fails to initialize itself and
    it's default handler method. We use this in further tests below."""

    def __init__(self):
        pass


class UMFRouterTests(unittest.TestCase):
    """UMFRouterTests suite. Test that message handlers can be registered
    with the UMRouter and that message can indeed be routed."""

    def chat_handler(self, message, ws):
        """Mock chat handler."""
        print('Processing message of type: %s' % message['type'])

    def test_creating_two_umf_routers_results_in_one_instance(self):
        """Assert that attempting to create two UMFRouters does not
        result in two new instances. The expectation is that we'll get one
        instance confirming the singleton's behavior."""
        umf = UMFRouter()
        second_umf = UMFRouter()
        self.assertEqual(umf, second_umf,
                         msg='First UMFRouter instance should be the same as '
                             'the second UMFRouter instance')

    def test_that_handlers_can_be_registered(self):
        """Assert that handlers can be registered. The result of this test
        should be an increase in the number of handlers for a given type,
        whereby proving successful registration."""
        umf = UMFRouter()
        initial_chat_handler_count = umf.handler_count(
            UMFMessageType.CHAT)
        umf.register_handler(UMFMessageType.CHAT, self.chat_handler)
        self.assertTrue(umf.handler_count(UMFMessageType.CHAT) ==
                        initial_chat_handler_count + 1,
                        msg='chat handler registration should have resulted '
                            'in type existing in message_router_map.')

    def test_that_routing_a_registered_message_is_successful(self):
        """Assert that a newly constructed message can be routed."""
        umf = UMFRouter()
        umf.register_handler(UMFMessageType.CHAT, self.chat_handler)
        msg = {
            UMFMessageField.MID: 0,
            UMFMessageField.TYPE: UMFMessageType.CHAT,
            UMFMessageField.TO: 'umfTestServer',
            UMFMessageField.FROM: 'UMFTester:abcd',
            UMFMessageField.VERSION: UMFMessageVersion.VERSION_1_0,
            UMFMessageField.TIMESTAMP: '',
            UMFMessageField.BODY: {
            }
        }
        routed = umf.route(msg, None)
        self.assertTrue(routed, msg='msg routing for message of type chat '
                                    'was expected to be routed to a handler.')

    def test_that_attempting_to_route_an_unregistered_message_fails(self):
        """Assert that if we fail to register a message and then attempt to
        route it then it will fail to route."""
        umf = UMFRouter()

        msg = {
            UMFMessageField.MID: 0,
            UMFMessageField.TYPE: 'badtype',
            UMFMessageField.TO: 'umfTestServer',
            UMFMessageField.FROM: 'UMFTester:abcd',
            UMFMessageField.VERSION: UMFMessageVersion.VERSION_1_0,
            UMFMessageField.TIMESTAMP: '',
            UMFMessageField.BODY: {
            }
        }
        routed = umf.route(msg, None)
        self.assertFalse(routed, msg='msg routing for message of type badtype '
                                     'was expected to NOT be routed to a '
                                     'handler.')

    def test_that_handler_class_with_missing_handler_throws_exception(self):
        """Assert that a message handler without a handler method raises an
        exception."""
        with self.assertRaises(Exception, msg='Message class with '
                                              'missing handler should raise an '
                                              'exception'):
            bad_handler = BadHandler()
            bad_handler.handler({})


if __name__ == '__main__':
    unittest.main()
