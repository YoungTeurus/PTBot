from typing import Callable

from chat.ChatMessage import ChatMessage
from games.mafia.WaitMessageSettings import WAIT_MESSAGE_PROCESSOR
from utils.Utils import CALLBACK_FUNCTION


class MafiaAction:
    pass


class WaitBeforeNextAction(MafiaAction):
    timeoutSecs: float

    def __init__(self, timeoutSecs: float):
        self.timeoutSecs = timeoutSecs


class SendGlobalMessage(MafiaAction):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg


class SendWhisperMessage(MafiaAction):
    msg: str
    receiver: str

    def __init__(self, msg: str, receiver: str):
        self.msg = msg
        self.receiver = receiver


class WaitForAnswer(MafiaAction):
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


# ({player_name => answer}) => None
WAIT_FOR_ANSWER_FROM_MANY_CALLBACK = Callable[[dict[str, ChatMessage]], None]


class WaitForAnswerFromMany(MafiaAction):
    desiredSenders: list[str]
    timeoutSecs: float
    # ( (nick => message) ) => None
    onAnswers: WAIT_FOR_ANSWER_FROM_MANY_CALLBACK

    def __init__(self, desiredSenders: list[str], timeoutSecs: float,
                 onAnswers: WAIT_FOR_ANSWER_FROM_MANY_CALLBACK) -> None:
        self.desiredSenders = desiredSenders
        self.timeoutSecs = timeoutSecs
        self.onAnswers = onAnswers
