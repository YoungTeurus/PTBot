from collections import Callable
from enum import Enum
from threading import Thread, Lock
from time import sleep

from games.mafia.MafiaWorker import MafiaWorker
from utils.Utils import STRING_CONSUMER, CALLBACK_FUNCTION


class MafiaAction(Enum):
    SEND_GLOBAL_MESSAGE = 0
    SEND_WHISPER_TO_PLAYER = 1
    WAIT_FOR_ANSWER_FROM_PLAYERS = 2


class MafiaAction:
    def perform(self, mafiaWorker: MafiaWorker) -> None:
        raise NotImplementedError


class SendGlobalMessage(MafiaAction):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg

    def perform(self, mafiaWorker: MafiaWorker) -> None:
        mafiaWorker.globalMessage(self.msg)


class SendWhisperMessage(MafiaAction):
    msg: str
    receiver: str

    def __init__(self, msg: str, to: str):
        self.msg = msg
        self.receiver = to

    def perform(self, mafiaWorker: MafiaWorker) -> None:
        mafiaWorker.whisperMessage(self.msg, self.receiver)


class WaitForAnswer(MafiaAction):
    desiredSender: str
    timeoutSecs: float
    onAnswerReceived: STRING_CONSUMER
    onAnswerNotReceived: CALLBACK_FUNCTION

    def __init__(self, desiredSender: str, timeoutSecs: float,
                 onAnswerReceived: STRING_CONSUMER, onAnswerNotReceived: CALLBACK_FUNCTION) -> None:
        self.desiredSender = desiredSender
        self.timeoutSecs = timeoutSecs
        self.onAnswerReceived = onAnswerReceived
        self.onAnswerNotReceived = onAnswerNotReceived

    def perform(self, mafiaWorker: MafiaWorker) -> None:
        mafiaWorker.waitForAnswer(self.desiredSender, self.timeoutSecs, self.onAnswerReceived, self.onAnswerNotReceived)


WAIT_FOR_ANSWER_FROM_MANY_CALLBACK = Callable[[dict[str, str]], None]


class MutableInt:
    value: int

    def __init__(self, value: int):
        self.value = value

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

    def perform(self, mafiaWorker: MafiaWorker) -> None:
        answers = {}

        # Количество ответов, которое мы ожидаем:
        lock = Lock()
        answersNeeded: MutableInt = MutableInt(len(self.desiredSenders))

        def getAddAnswerConsumer(player: str) -> STRING_CONSUMER:
            def wrapper(answer: str) -> None:
                answers[player] = answer
                with lock:
                    answersNeeded.value -= 1
            return wrapper

        def getAddNotAnsweredCallback(player: str) -> CALLBACK_FUNCTION:
            def wrapper() -> None:
                answers[player] = None
                with lock:
                    answersNeeded.value -= 1
            return wrapper

        for desiredSender in self.desiredSenders:
            mafiaWorker.waitForAnswer(desiredSender, self.timeoutSecs,
                                      getAddAnswerConsumer(desiredSender),
                                      getAddNotAnsweredCallback(desiredSender))

        def waitForAllAnswers() -> None:
            while True:
                sleep(0.5)
                with lock:
                    if answersNeeded.value > 0:
                        continue
                return self.onAnswers(answers)

        thread = Thread(target=waitForAllAnswers, daemon=True)
        thread.start()
