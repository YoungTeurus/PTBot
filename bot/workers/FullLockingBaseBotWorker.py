from bot.workers.BaseBotWorker import BaseBotWorker


class FullLockingBaseBotWorker(BaseBotWorker):
    def __init__(self):
        super().__init__()

    def _doWork(self) -> None:
        with self.lock:
            if self.hasWork():
                self.doWork()
