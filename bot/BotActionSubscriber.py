import time
from threading import Lock, Thread

from chat.ChatSenderController import ChatSenderController


class BaseBotWorker:
    def prepare(self, lock: Lock):
        pass

    def interupt(self):
        pass


class ChatSenderWorker(BaseBotWorker, Thread):
    running: bool
    lock: Lock
    chatSenderController: ChatSenderController
    lastMessageTime: float
    secsBetweenMessages: float = 1

    def __init__(self, chatSenderController: ChatSenderController):
        super(ChatSenderWorker, self).__init__()
        self.running = False
        self.chatSenderController = chatSenderController

    def prepare(self, lock: Lock):
        self.lastMessageTime = time.time()
        self.lock = lock
        self.running = True
        self.start()

    def run(self) -> None:
        while self.running:
            if self.hasWork():
                with self.lock:
                    self.doWork()

    def hasWork(self) -> bool:
        return len(self.chatSenderController.sendQuery) > 0 and (time.time() - self.lastMessageTime) > self.secsBetweenMessages

    def doWork(self) -> None:
        self.chatSenderController.sendNextMessage()
        self.lastMessageTime = time.time()
        print("Sent msg! Waiting for {} secs...".format(self.secsBetweenMessages))

    def interupt(self):
        self.running = False


class BotActionProcessor:
    lock: Lock
    workers: list[BaseBotWorker]

    def __init__(self):
        self.lock = Lock()
        self.workers = []

    def addWorker(self, worker: BaseBotWorker) -> None:
        self.workers.append(worker)
        worker.prepare(self.lock)

    def stopAll(self) -> None:
        for worker in self.workers:
            worker.interupt()
