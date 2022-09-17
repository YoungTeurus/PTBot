from workers.interfaces.BaseBotWorker import BaseBotWorker


class NonLockingBaseBotWorker(BaseBotWorker):
    def _doWhileRunning(self) -> None:
        if self.hasWork():
            self.doWork()
