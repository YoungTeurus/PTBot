from games.mafia.logic.NewMafiaAction import OneTimeAction


class StartNewDay(OneTimeAction):
    def _setup(self) -> None:
        self.worker.game.nextDay()