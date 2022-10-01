from enum import Enum

from chat.ChatMessage import ChatMessage


class NotifyAction(Enum):
    CONTINUE_TO_NEXT_OBSERVER = 1
    END_NOTIFY_CHAIN = 2


class ChatObserver:
    def startObserving(self) -> None:
        """
        Выполняется после добавления наблюдателя в контейнер наблюдателей
        """
        pass

    def notify(self, msg: ChatMessage) -> NotifyAction:
        pass

    def endObserving(self) -> None:
        """
        Выполняется после удаления наблюдателя из контейнера наблюдателей
        """
        pass