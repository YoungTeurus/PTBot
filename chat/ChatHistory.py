from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver


MAX_HISTORY_SIZE = 500

class ChatHistory:
    history: list[ChatMessage]
    observers: list[ChatObserver]

    def __init__(self):
        self.history = []
        self.observers = []

    def addObserver(self, observer: ChatObserver) -> None:
        self.observers.append(observer)

    def appendHistoryMultipleAndClean(self, msgs: list[ChatMessage]) -> None:
        if len(self.history) + len(msgs) > MAX_HISTORY_SIZE:
            self.history.clear()
        for msg in msgs:
            self.appendHistory(msg)

    def appendHistory(self, msg: ChatMessage) -> None:
        for obs in self.observers:
            obs.notify(msg)
        self.history.append(msg)
