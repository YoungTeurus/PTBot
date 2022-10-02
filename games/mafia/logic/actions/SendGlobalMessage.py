from games.mafia.logic.NewMafiaAction import OneTimeAction


class SendGlobalMessage(OneTimeAction):
    msg: str

    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg

    def _setup(self) -> None:
        self.worker.globalMessage(self.msg)
