from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction


class SelfAwareChatObserver(ChatObserver):
    def notify(self, msg: ChatMessage) -> NotifyAction:
        if msg.type.sentByBot:
            return self.doOnOwnMessage(msg)
        else:
            return self.doOnOtherMessage(msg)

    def doOnOwnMessage(self, msg: ChatMessage) -> NotifyAction:
        pass

    def doOnOtherMessage(self, msg: ChatMessage) -> NotifyAction:
        pass
