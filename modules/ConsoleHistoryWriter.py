from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver


class ConsoleHistoryWriter(ChatObserver):
    def notify(self, msg: ChatMessage):
        print(msg)
