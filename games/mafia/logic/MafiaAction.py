import time
from typing import Callable, Optional

from chat.ChatMessage import ChatMessage
from games.mafia.WaitMessageSettings import WAIT_MESSAGE_PROCESSOR
from utils.Utils import CALLBACK_FUNCTION


class MafiaAction:
    pass


class LockingMafiaAction(MafiaAction):
    """
    Действия, для которых нужно дождаться их завершения, чтобы перейти к следующему
    """


class NoStateMutationMafiaAction(MafiaAction):
    """
    Действия, которые не изменяют состояния игры и могут выполняться сразу
    """
    pass


class StartNewNight(MafiaAction):
    pass


class StartNewDay(MafiaAction):
    pass


class KillPlayer(MafiaAction):
    victim: str
    reason: str

    def __init__(self, victim: str, reason: str) -> None:
        self.victim = victim
        self.reason = reason


class WaitBeforeNextAction(LockingMafiaAction):
    startWaitTime: Optional[float]
    endWaitTime: Optional[float]
    timeoutSecs: float
    onTimeoutEnd: Optional[CALLBACK_FUNCTION]

    def __init__(self, timeoutSecs: float, onTimeoutEnd: CALLBACK_FUNCTION = None):
        self.startWaitTime = None
        self.endWaitTime = None
        self.timeoutSecs = timeoutSecs
        self.onTimeoutEnd = onTimeoutEnd

    def startWait(self) -> None:
        self.startWaitTime = time.time()
        self.endWaitTime = self.startWaitTime + self.timeoutSecs

    def isWaitEnded(self) -> bool:
        return time.time() >= self.endWaitTime

class SendGlobalMessage(NoStateMutationMafiaAction):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg


class SendWhisperMessage(NoStateMutationMafiaAction):
    msg: str
    receiver: str

    def __init__(self, msg: str, receiver: str):
        self.msg = msg
        self.receiver = receiver


class WaitForAnswer(LockingMafiaAction):
    desiredSender: str
    timeoutSecs: float
    onAnswerReceived: WAIT_MESSAGE_PROCESSOR
    onAnswerNotReceived: CALLBACK_FUNCTION

    def __init__(self, desiredSender: str, timeoutSecs: float,
                 onAnswerReceived: WAIT_MESSAGE_PROCESSOR, onAnswerNotReceived: CALLBACK_FUNCTION) -> None:
        self.desiredSender = desiredSender
        self.timeoutSecs = timeoutSecs
        self.onAnswerReceived = onAnswerReceived
        self.onAnswerNotReceived = onAnswerNotReceived


# {player_name => answer}
ANSWERS_DICT = dict[str, ChatMessage]
WAIT_FOR_ANSWER_FROM_MANY_CALLBACK = Callable[[ANSWERS_DICT], None]


class WaitForAnswerFromMany(LockingMafiaAction):
    desiredSenders: list[str]
    timeoutSecs: float
    # ( (nick => message) ) => None
    onAnswers: WAIT_FOR_ANSWER_FROM_MANY_CALLBACK
    onAnswerValidator: Optional[WAIT_MESSAGE_PROCESSOR]
    onEachAnswerAfterValidation: Optional[WAIT_MESSAGE_PROCESSOR]

    def __init__(self, desiredSenders: list[str], timeoutSecs: float,
                 onAnswers: WAIT_FOR_ANSWER_FROM_MANY_CALLBACK, onAnswerValidator: WAIT_MESSAGE_PROCESSOR = None,
                 onEachAnswerAfterValidation: WAIT_MESSAGE_PROCESSOR = None) -> None:
        self.desiredSenders = desiredSenders
        self.timeoutSecs = timeoutSecs
        self.onAnswers = onAnswers
        self.onAnswerValidator = onAnswerValidator
        self.onEachAnswerAfterValidation = onEachAnswerAfterValidation
