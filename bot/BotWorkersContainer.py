from threading import Lock

from bot.workers.BaseBotWorker import BaseBotWorker


class BotWorkersContainer:
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
            worker.interrupt()
