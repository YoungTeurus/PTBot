from time import time

from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from properties import CHAT_SENDER_WORKER
from utils.ConsoleProvider import CONSOLE
from workers.base.WorkLockingBaseBotWorker import WorkLockingBaseBotWorker


class ChatSenderWorker(WorkLockingBaseBotWorker):
    chatSenderController: ChatSenderQuerySender
    lastMessageTime: float
    secsBetweenMessages: float = CHAT_SENDER_WORKER["secsBetweenMessages"]

    def __init__(self, chatSenderController: ChatSenderQuerySender):
        super().__init__()
        self.chatSenderController = chatSenderController

    def preInit(self) -> None:
        self.lastMessageTime = time()

    def hasWork(self) -> bool:
        return self.chatSenderController.hasMsgs() and \
               (time() - self.lastMessageTime) > self.secsBetweenMessages

    def doWork(self) -> None:
        self.chatSenderController.sendNextMessage()
        self.lastMessageTime = time()
