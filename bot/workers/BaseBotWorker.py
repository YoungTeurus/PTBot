from threading import Lock, Thread


class BaseBotWorker(Thread):
    lock: Lock
    running: bool

    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = False

    def prepare(self, lock: Lock):
        self.lock = lock
        self.running = True
        self.start()

    def run(self) -> None:
        while self.running:
            if self.hasWork():
                with self.lock:
                    self.doWork()

    def hasWork(self) -> bool:
        return False

    def doWork(self) -> None:
        pass

    def interrupt(self):
        self.running = False
