from threading import Lock, Thread


class BaseBotWorker(Thread):
    lock: Lock
    running: bool

    def __init__(self):
        super().__init__()
        self.daemon = False
        self.running = False

    def prepare(self, lock: Lock) -> None:
        print("Worker '{}' is preparing".format(self))
        self.preInit()

        self.lock = lock
        self.running = True
        self.start()

        self.postInit()
        print("Worker '{}' is prepared".format(self))

    def preInit(self) -> None:
        pass

    def postInit(self) -> None:
        pass

    def run(self) -> None:
        print("Worker '{}' began to run".format(self))
        while self.running:
            self._doWhileRunning()

    def hasWork(self) -> bool:
        return False

    def _doWhileRunning(self) -> None:
        pass

    def doWork(self) -> None:
        pass

    def interrupt(self):
        print("Worker '{}' is interrupted".format(self))
        self.running = False
