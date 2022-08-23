from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction
from chat.ChatSenderQuerySender import ChatSenderQuerySender


class Parrot(ChatObserver):
    def __init__(self, csqs: ChatSenderQuerySender):
        self.csqs = csqs

    def notify(self, msg: ChatMessage) -> NotifyAction:
        if msg.sender != "- Ma-Zee-ic -":
            self.csqs.addMessageToQuery('{} сказал(а) {}'.format(msg.sender, msg.body))
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
