from games.mafia.logic.NewMafiaAction import OneTimeAction


class KillPlayer(OneTimeAction):
    victim: str
    reason: str

    def __init__(self, victim: str, reason: str) -> None:
        super().__init__()
        self.victim = victim
        self.reason = reason

    def _setup(self) -> None:
        # TODO: Убийство игрока
        pass