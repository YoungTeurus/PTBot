from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver


class ChatHistory:
    history: list[ChatMessage]
    observers: list[ChatObserver]

    def __init__(self):
        self.history = []
        self.observers = []

    def addObserver(self, observer: ChatObserver) -> None:
        self.observers.append(observer)

    def appendHistory(self, msg: ChatMessage) -> None:
        for obs in self.observers:
            obs.notify(msg)
        self.history.append(msg)
