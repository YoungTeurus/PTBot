from threading import Lock, Thread

from properties import LOGGING
from utils.ConsoleProvider import CONSOLE


class BaseBotWorker(Thread):
    lock: Lock
    running: bool

    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = False

    def prepare(self, lock: Lock) -> None:
        if LOGGING.logWorkers:
            CONSOLE.print("Worker '{}' is preparing".format(self))
        self.preInit()

        self.lock = lock
        self.running = True
        self.start()

        self.postInit()
        if LOGGING.logWorkers:
            CONSOLE.print("Worker '{}' is prepared".format(self))

    def preInit(self) -> None:
        pass

    def postInit(self) -> None:
        pass

    def run(self) -> None:
        if LOGGING.logWorkers:
            CONSOLE.print("Worker '{}' began to run".format(self))
        while self.running:
            self._doWhileRunning()
        if LOGGING.logWorkers:
            CONSOLE.print("Worker '{}' stopped".format(self))

    def hasWork(self) -> bool:
        return False

    def _doWhileRunning(self) -> None:
        pass

    def doWork(self) -> None:
        pass

    def interrupt(self):
        if LOGGING.logWorkers:
            CONSOLE.print("Worker '{}' is interrupted".format(self))
        self.running = False
        self.join()
