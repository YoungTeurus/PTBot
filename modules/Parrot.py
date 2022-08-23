from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver
from chat.ChatSenderQuerySender import ChatSenderQuerySender


class Parrot(ChatObserver):
    def __init__(self, csqs: ChatSenderQuerySender):
        self.csqs = csqs

    def notify(self, msg: ChatMessage):
        if msg.sender != "- Ma-Zee-ic -":
            self.csqs.addMessageToQuery('{} сказал(а) {}'.format(msg.sender, msg.body))
