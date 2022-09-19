from time import sleep

from workers.base.BaseBotWorker import BaseBotWorker


class WorkLockingBaseBotWorker(BaseBotWorker):
    def _doWhileRunning(self) -> None:
        if self.hasWork():
            with self.lock:
                self.doWork()
        else:
            sleep(0.1)
