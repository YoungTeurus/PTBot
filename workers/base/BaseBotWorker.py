from threading import Lock, Thread

from properties import LOGGING
from utils.ConsoleProvider import ConsoleProvider


class BaseBotWorker(Thread):
    lock: Lock
    running: bool
    cp: ConsoleProvider

    def __init__(self, cp: ConsoleProvider):
        super().__init__()
        self.daemon = True
        self.running = False
        self.cp = cp

    def prepare(self, lock: Lock) -> None:
        if LOGGING.logWorkers:
            self.cp.print("Worker '{}' is preparing".format(self))
        self.preInit()

        self.lock = lock
        self.running = True
        self.start()

        self.postInit()
        if LOGGING.logWorkers:
            self.cp.print("Worker '{}' is prepared".format(self))

    def preInit(self) -> None:
        pass

    def postInit(self) -> None:
        pass

    def run(self) -> None:
        if LOGGING.logWorkers:
            self.cp.print("Worker '{}' began to run".format(self))
        while self.running:
            self._doWhileRunning()
        if LOGGING.logWorkers:
            self.cp.print("Worker '{}' stopped".format(self))

    def hasWork(self) -> bool:
        return False

    def _doWhileRunning(self) -> None:
        pass

    def doWork(self) -> None:
        pass

    def interrupt(self, timeout: float = 1):
        if LOGGING.logWorkers:
            self.cp.print("Worker '{}' is interrupted".format(self))
        self.running = False
        self.join(timeout)
