from threading import Lock

from properties import LOGGING
from utils.ConsoleProvider import CONSOLE
from workers.base.BaseBotWorker import BaseBotWorker


class BotWorkersContainer:
    lock: Lock
    workers: list[BaseBotWorker]

    def __init__(self):
        self.lock = Lock()
        self.workers = []

    def add(self, worker: BaseBotWorker) -> None:
        with self.lock:
            self.workers.append(worker)
            if LOGGING.logWorkers:
                CONSOLE.print("Worker '{}' was added".format(worker))
            worker.prepare(self.lock)

    def stopAll(self) -> None:
        if LOGGING.logWorkers:
            CONSOLE.print("Stopping all workers...")
        for worker in self.workers:
            worker.interrupt()
        if LOGGING.logWorkers:
            CONSOLE.print("All workers were stopped...")
