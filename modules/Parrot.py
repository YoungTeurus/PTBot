from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction
from chat.ChatSenderQuerySender import ChatSenderQuerySender
from chat.SelfAwareChatObserver import SelfAwareChatObserver


class Parrot(SelfAwareChatObserver):
    def __init__(self, csqs: ChatSenderQuerySender):
        self.csqs = csqs

    def doOnOtherMessage(self, msg: ChatMessage) -> NotifyAction:
        self.csqs.addMessageToQuery('{} сказал(а) {}'.format(msg.sender, msg.body))
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
