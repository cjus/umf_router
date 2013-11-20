"""Message
Init messages by loading and instanciating them here
"""

from chat_msg_handler import ChatMsgHandler
from client_msg_handler import ClientMsgHandler
from heart_msg_handler import HeartBeatMsgHandler
from mouse_msg_handler import MouseMsgHandler

ChatMsgHandler()
ClientMsgHandler()
HeartBeatMsgHandler()
MouseMsgHandler()
