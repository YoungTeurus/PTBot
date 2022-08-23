from bot.workers.BaseBotWorker import BaseBotWorker


class WorkLockingBaseBotWorker(BaseBotWorker):
    def __init__(self):
        super().__init__()

    def _doWork(self) -> None:
        if self.hasWork():
            with self.lock:
                self.doWork()
