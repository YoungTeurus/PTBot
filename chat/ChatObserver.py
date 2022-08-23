from enum import Enum

from chat.ChatMessage import ChatMessage


class NotifyAction(Enum):
    CONTINUE_TO_NEXT_OBSERVER = 1
    END_NOTIFY_CHAIN = 2


class ChatObserver:
    def notify(self, msg: ChatMessage) -> NotifyAction:
        pass
