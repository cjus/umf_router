import unittest
from umf_router import UMFRouter

__author__ = 'carlosjustiniano'


class UMFRouterTests(unittest.TestCase):
    def setUp(self):
        pass

    def chat_handler(self, message):
        print "Processing message of type: %s" % message["type"]
        return True

    def heart_beat_handler(self, message):
        print "Processing message of type: %s" % message["type"]
        return True

    def test_singleton_behavior(self):
        umf1 = UMFRouter()
        umf2 = UMFRouter()
        self.assertEqual(umf1, umf2, msg="umf1 and umf2 should be equal")

    def test_handler_registration(self):
        umf = UMFRouter()
        registered = umf.register_handler("chat", self.chat_handler)
        self.assertTrue(registered, msg="chat handler registration was expected to succeed")

        registered = umf.register_handler("chat", self.chat_handler)
        self.assertFalse(registered,
                         msg="chat handler registration was expected to fail since it has already been registered")

    def test_message_routing(self):
        umf = UMFRouter()
        umf.register_handler("chat", self.chat_handler)
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
        routed = umf.route(msg)
        self.assertTrue(routed, msg="msg routing for message of type chat was expected to be routed")


if __name__ == '__main__':
    unittest.main()
