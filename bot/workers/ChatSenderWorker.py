from time import time
from threading import Lock

from bot.workers.BaseBotWorker import BaseBotWorker
from chat.ChatSenderQuerySender import ChatSenderQuerySender


class ChatSenderWorker(BaseBotWorker):
    chatSenderController: ChatSenderQuerySender
    lastMessageTime: float
    secsBetweenMessages: float = 1

    def __init__(self, chatSenderController: ChatSenderQuerySender):
        super(ChatSenderWorker, self).__init__()
        self.chatSenderController = chatSenderController

    def prepare(self, lock: Lock):
        self.lastMessageTime = time()
        super().prepare(lock)

    def hasWork(self) -> bool:
        return len(self.chatSenderController.sendQuery) > 0 and\
               (time() - self.lastMessageTime) > self.secsBetweenMessages

    def doWork(self) -> None:
        self.chatSenderController.sendNextMessage()
        self.lastMessageTime = time()
        print("Sent msg! Waiting for {} secs...".format(self.secsBetweenMessages))