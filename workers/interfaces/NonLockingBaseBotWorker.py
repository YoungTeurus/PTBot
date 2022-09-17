from workers.interfaces.BaseBotWorker import BaseBotWorker


class NonLockingBaseBotWorker(BaseBotWorker):
    def _doWork(self) -> None:
        if self.hasWork():
            self.doWork()
