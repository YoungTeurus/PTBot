from games.mafia.logic.NewMafiaAction import OneTimeAction


class StartNewNight(OneTimeAction):
    def _setup(self) -> None:
        self.worker.game.nextNight()