from chat.ChatMessage import ChatMessage
from games.mafia.WaitMessageSettings import WAIT_MESSAGE_PROCESSOR, WaitMessageSettings, \
    WAIT_MESSAGE_ON_TIMEOUT_CALLBACK
from games.mafia.logic.NewMafiaAction import CompletableMafiaAction


class WaitForAnswer(CompletableMafiaAction):
    desiredSender: str
    timeoutSecs: float
    onAnswerReceived: WAIT_MESSAGE_PROCESSOR
    onAnswerNotReceived: WAIT_MESSAGE_ON_TIMEOUT_CALLBACK

    def __init__(self, desiredSender: str, timeoutSecs: float,
                 onAnswerReceived: WAIT_MESSAGE_PROCESSOR,
                 onAnswerNotReceived: WAIT_MESSAGE_ON_TIMEOUT_CALLBACK) -> None:
        super().__init__()
        self.desiredSender = desiredSender
        self.timeoutSecs = timeoutSecs
        self.onAnswerReceived = onAnswerReceived
        self.onAnswerNotReceived = onAnswerNotReceived

    def __onAnswerReceived(self, msg: ChatMessage) -> bool:
        endWait = self.onAnswerReceived(msg)
        if endWait:
            self.complete()
        return endWait

    def __onAnswerNotReceived(self, nickname: str) -> None:
        self.onAnswerNotReceived(nickname)
        self.complete()

    def _setup(self) -> None:
        wms = WaitMessageSettings(self.timeoutSecs,
                                  self.__onAnswerReceived,
                                  self.__onAnswerNotReceived)
        self.worker.waitForAnswer(self.desiredSender, wms)

    def _update(self) -> None:
        pass
