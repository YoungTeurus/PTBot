from threading import Lock
from typing import Callable, Optional

from chat.ChatMessage import ChatMessage
from games.mafia.WaitMessageSettings import WAIT_MESSAGE_PROCESSOR, WAIT_MESSAGE_ON_TIMEOUT_CALLBACK, \
    WaitMessageSettings
from games.mafia.logic.NewMafiaAction import CompletableMafiaAction
from utils.Utils import MutableInt

# {player_name => answer}
ANSWERS_DICT = dict[str, Optional[ChatMessage]]
WAIT_FOR_ANSWER_FROM_MANY_CALLBACK = Callable[[ANSWERS_DICT], None]


class WaitForAnswerFromMany(CompletableMafiaAction):
    desiredSenders: list[str]
    timeoutSecs: float
    # Вызывается после получения всех ответов:
    # ( (nick => message) ) => None
    onAllAnswers: WAIT_FOR_ANSWER_FROM_MANY_CALLBACK
    # Вызывается перед сохранением каждого ответа. Если вернёт False - ответ не будет принят и ожидание продолжится.
    onAnswerValidator: Optional[WAIT_MESSAGE_PROCESSOR]
    # Вызывается в случае таймаута для каждого отправителя, что вызвал таймаут:
    onEachAnswerTimeout: Optional[WAIT_MESSAGE_ON_TIMEOUT_CALLBACK]

    answers: ANSWERS_DICT
    lock: Lock
    answersNeeded: MutableInt

    def __init__(self, desiredSenders: list[str], timeoutSecs: float,
                 onAllAnswers: WAIT_FOR_ANSWER_FROM_MANY_CALLBACK,
                 onAnswerValidator: WAIT_MESSAGE_PROCESSOR = None,
                 onEachAnswerTimeout: WAIT_MESSAGE_ON_TIMEOUT_CALLBACK = None) -> None:
        super().__init__()
        self.desiredSenders = desiredSenders
        self.timeoutSecs = timeoutSecs
        self.onAllAnswers = onAllAnswers
        self.onAnswerValidator = onAnswerValidator
        self.onEachAnswerTimeout = onEachAnswerTimeout

    def onNewAnswer(self, msg: ChatMessage) -> bool:
        if self.onAnswerValidator is not None and not self.onAnswerValidator(msg):
            return False  # Если ответ не прошёл валидацию, продолжаем ждать ответа
        self.answers[msg.sender] = msg
        with self.lock:
            self.answersNeeded.value -= 1
        return True

    def onNotAnswered(self, player: str) -> None:
        if self.onEachAnswerTimeout is not None:
            self.onEachAnswerTimeout(player)
        self.answers[player] = None
        with self.lock:
            self.answersNeeded.value -= 1

    def _setup(self) -> None:
        self.answers = {}
        self.lock = Lock()
        self.answersNeeded = MutableInt(len(self.desiredSenders))

        for desiredSender in self.desiredSenders:
            wms = WaitMessageSettings(self.timeoutSecs,
                                      self.onNewAnswer,
                                      self.onNotAnswered)
            self.worker.waitForAnswer(desiredSender, wms)

    def _update(self) -> None:
        with self.lock:
            if self.answersNeeded.value == 0:
                self.onAllAnswers(self.answers)
                self.complete()
