from workers.interfaces.BaseBotWorker import BaseBotWorker


class FullLockingBaseBotWorker(BaseBotWorker):
    def _doWhileRunning(self) -> None:
        with self.lock:
            if self.hasWork():
                self.doWork()
