import time

from games.mafia.logic.NewMafiaAction import CompletableMafiaAction


class WaitBeforeNextAction(CompletableMafiaAction):
    timeoutSecs: float

    startWaitTime: float
    endWaitTime: float

    def __init__(self, timeoutSecs: float) -> None:
        super().__init__()
        self.timeoutSecs = timeoutSecs

    def _setup(self) -> None:
        self.startWaitTime = time.time()
        self.endWaitTime = self.startWaitTime + self.timeoutSecs

    def _update(self) -> None:
        if time.time() >= self.endWaitTime:
            self.complete()
