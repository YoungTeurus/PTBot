from bot.workers.BaseBotWorker import BaseBotWorker


class NonLockingBaseBotWorker(BaseBotWorker):
    def __init__(self):
        super().__init__()

    def _doWork(self) -> None:
        if self.hasWork():
            self.doWork()
