from workers.interfaces.BaseBotWorker import BaseBotWorker


class FullLockingBaseBotWorker(BaseBotWorker):
    def _doWork(self) -> None:
        with self.lock:
            if self.hasWork():
                self.doWork()
