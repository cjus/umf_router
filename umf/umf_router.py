"""
"""


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


@singleton
class UMFRouter:
    def __init__(self):
        self.message_router_map = {}

    def register_handler(self, message_type, handler):
        registered = False
        if message_type in self.message_router_map:
            if self.message_router_map[message_type] == handler:
                return registered
        else:
            self.message_router_map[message_type] = []
            registered = True
        self.message_router_map[message_type].append(handler)
        print "    Handler registered for %s by %s" % (message_type, handler)
        return registered

    def route(self, message):
        routed = False
        if message["type"] not in self.message_router_map:
            print "Unable to route message. Message handler not registered for message type: %s" % message["type"]
            return routed

        for handler in self.message_router_map[message["type"]]:
            print "Message of type %s is being routed to handler %s" % (message["type"], handler)
            routed = True
            handler(message)

        return routed

