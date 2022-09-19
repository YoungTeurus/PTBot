from time import sleep

from workers.base.BaseBotWorker import BaseBotWorker


class FullLockingBaseBotWorker(BaseBotWorker):
    def _doWhileRunning(self) -> None:
        with self.lock:
            if self.hasWork():
                self.doWork()
            else:
                sleep(0.1)
