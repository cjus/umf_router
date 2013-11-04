"""
"""


class UMFRouter():
    message_router_map = {}

    def register_handler(self, message_type, handler):
        if message_type not in self.message_router_map:
            self.message_router_map[message_type] = []
        self.message_router_map[message_type].append(handler)

    def route(self, message):
        for handler in self.message_router_map[message.type]:
            handler(message)

