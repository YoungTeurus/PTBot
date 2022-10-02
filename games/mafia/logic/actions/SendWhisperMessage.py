from games.mafia.logic.NewMafiaAction import OneTimeAction


class SendWhisperMessage(OneTimeAction):
    msg: str
    receiver: str

    def __init__(self, msg: str, receiver: str) -> None:
        super().__init__()
        self.msg = msg
        self.receiver = receiver

    def _setup(self) -> None:
        self.worker.whisperMessage(self.msg, self.receiver)
