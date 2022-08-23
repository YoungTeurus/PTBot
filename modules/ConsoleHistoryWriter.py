from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction


class ConsoleHistoryWriter(ChatObserver):
    def notify(self, msg: ChatMessage) -> NotifyAction:
        print(msg)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
