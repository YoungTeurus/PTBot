from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.SelfAwareChatObserver import SelfAwareChatObserver
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender


class Parrot(SelfAwareChatObserver):
    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory):
        self.csqs = csqs
        self.ocmf = ocmf

    def doOnOtherMessage(self, msg: ChatMessage) -> NotifyAction:
        self.csqs.addGlobalMessage('{} сказал(а) {}'.format(msg.sender, msg.body), self.ocmf)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
