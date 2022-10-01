from __future__ import annotations

from threading import Lock, Thread
from time import sleep
from typing import Callable, Type, Optional, TYPE_CHECKING

from chat.ChatMessage import ChatMessage
from games.mafia.WaitMessageSettings import WaitMessageSettings, WAIT_MESSAGE_PROCESSOR

if TYPE_CHECKING:
    from games.mafia.MafiaWorker import MafiaWorker
from games.mafia.logic.MafiaAction import MafiaAction, WaitBeforeNextAction, SendGlobalMessage, SendWhisperMessage, \
    WaitForAnswer, WaitForAnswerFromMany
from utils.Utils import MutableInt, CALLBACK_FUNCTION


def waitBeforeNextAction(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, WaitBeforeNextAction):
        mafiaWorker.waitBeforeNextActionSecs = action.timeoutSecs


def sendGlobalMessage(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, SendGlobalMessage):
        mafiaWorker.globalMessage(action.msg)


def sendWhisperMessage(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, SendWhisperMessage):
        mafiaWorker.whisperMessage(action.msg, action.receiver)


def waitForAnswer(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, WaitForAnswer):
        wms = WaitMessageSettings(action.timeoutSecs, action.onAnswerReceived,
                                  action.onAnswerNotReceived)
        mafiaWorker.waitForAnswer(action.desiredSender, wms)


def waitForAnswerFromMany(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, WaitForAnswerFromMany):
        answers: dict[str, Optional[ChatMessage]] = {}

        lock = Lock()
        # Количество ответов, которое мы ожидаем:
        answersNeeded: MutableInt = MutableInt(len(action.desiredSenders))

        def getAddAnswerConsumer(player: str) -> WAIT_MESSAGE_PROCESSOR:
            def wrapper(msg: ChatMessage) -> bool:
                answers[player] = msg
                with lock:
                    answersNeeded.value -= 1
                return True

            return wrapper

        def getAddNotAnsweredCallback(player: str) -> CALLBACK_FUNCTION:
            def wrapper() -> None:
                answers[player] = None
                with lock:
                    answersNeeded.value -= 1

            return wrapper

        for desiredSender in action.desiredSenders:
            wms = WaitMessageSettings(action.timeoutSecs, getAddAnswerConsumer(desiredSender),
                                      getAddNotAnsweredCallback(desiredSender))
            mafiaWorker.waitForAnswer(desiredSender, wms)

        def waitForAllAnswers() -> None:
            while True:
                sleep(0.5)
                with lock:
                    if answersNeeded.value > 0:
                        continue
                return action.onAnswers(answers)

        thread = Thread(target=waitForAllAnswers, daemon=True)
        thread.start()


ACTION_TYPE_TO_WORKER_ACTION: dict[Type[MafiaAction], Callable[[MafiaAction, MafiaWorker], None]] = {
    WaitBeforeNextAction: waitBeforeNextAction,
    SendGlobalMessage: sendGlobalMessage,
    SendWhisperMessage: sendWhisperMessage,
    WaitForAnswer: waitForAnswer,
    WaitForAnswerFromMany: waitForAnswerFromMany,
}
