from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction

MAX_HISTORY_SIZE = 500


class ChatProvider:
    history: list[ChatMessage]
    observers: list[ChatObserver]

    def __init__(self):
        self.history = []
        self.observers = []

    def addObserver(self, observer: ChatObserver) -> None:
        self.observers.append(observer)
        observer.startObserving()

    def removeObserver(self, observer: ChatObserver) -> None:
        self.observers.remove(observer)
        observer.endObserving()

    def cleanAndAddMultipleMessages(self, msgs: list[ChatMessage]) -> None:
        if len(self.history) + len(msgs) > MAX_HISTORY_SIZE:
            self.history.clear()
        for msg in msgs:
            self.__addMessage(msg)

    def __addMessage(self, msg: ChatMessage) -> None:
        for obs in self.observers:
            result: NotifyAction = obs.notify(msg)
            if result == NotifyAction.END_NOTIFY_CHAIN:
                break
        self.history.append(msg)
