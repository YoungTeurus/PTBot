from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction
from utils.ConsoleProvider import CONSOLE


class ChatToConsoleLogger(ChatObserver):
    def notify(self, msg: ChatMessage) -> NotifyAction:
        CONSOLE.print(msg)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
