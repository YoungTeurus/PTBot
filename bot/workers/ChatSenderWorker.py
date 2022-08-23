from time import time
from threading import Lock

from bot.workers.WorkLockingBaseBotWorker import WorkLockingBaseBotWorker
from chat.ChatSenderQuerySender import ChatSenderQuerySender
from properties import CHAT_SENDER_WORKER


class ChatSenderWorker(WorkLockingBaseBotWorker):
    chatSenderController: ChatSenderQuerySender
    lastMessageTime: float
    secsBetweenMessages: float = CHAT_SENDER_WORKER["secsBetweenMessages"]

    def __init__(self, chatSenderController: ChatSenderQuerySender):
        super().__init__()
        self.chatSenderController = chatSenderController

    def prepare(self, lock: Lock):
        self.lastMessageTime = time()
        super().prepare(lock)

    def hasWork(self) -> bool:
        return self.chatSenderController.hasMsgs() and \
               (time() - self.lastMessageTime) > self.secsBetweenMessages

    def doWork(self) -> None:
        self.chatSenderController.sendNextMessage()
        self.lastMessageTime = time()
