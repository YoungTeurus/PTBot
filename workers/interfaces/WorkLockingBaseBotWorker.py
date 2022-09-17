from workers.interfaces.BaseBotWorker import BaseBotWorker


class WorkLockingBaseBotWorker(BaseBotWorker):
    def _doWhileRunning(self) -> None:
        if self.hasWork():
            with self.lock:
                self.doWork()
