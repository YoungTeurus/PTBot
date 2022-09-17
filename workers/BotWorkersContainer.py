from threading import Lock

from properties import LOGGING
from utils.ConsoleProvider import ConsoleProvider
from workers.interfaces.BaseBotWorker import BaseBotWorker


class BotWorkersContainer:
    lock: Lock
    workers: list[BaseBotWorker]
    cp: ConsoleProvider

    def __init__(self, cp: ConsoleProvider):
        self.lock = Lock()
        self.workers = []
        self.cp = cp

    def add(self, worker: BaseBotWorker) -> None:
        with self.lock:
            self.workers.append(worker)
            if LOGGING.logWorkers:
                self.cp.print("Worker '{}' was added".format(worker))
            worker.prepare(self.lock)

    def stopAll(self) -> None:
        for worker in self.workers:
            worker.interrupt()