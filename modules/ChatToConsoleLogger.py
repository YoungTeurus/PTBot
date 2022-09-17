from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction
from utils.ConsoleProvider import ConsoleProvider


class ChatToConsoleLogger(ChatObserver):
    cp: ConsoleProvider

    def __init__(self, cp: ConsoleProvider):
        self.cp = cp

    def notify(self, msg: ChatMessage) -> NotifyAction:
        self.cp.print(msg)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
