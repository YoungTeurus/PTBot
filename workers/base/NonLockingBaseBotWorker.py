from time import sleep

from workers.base.BaseBotWorker import BaseBotWorker


class NonLockingBaseBotWorker(BaseBotWorker):
    def _doWhileRunning(self) -> None:
        if self.hasWork():
            self.doWork()
        else:
            sleep(0.1)
