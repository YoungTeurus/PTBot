from __future__ import annotations

from threading import Lock, Thread
from time import sleep
from typing import Callable, Type, Optional, TYPE_CHECKING

from chat.ChatMessage import ChatMessage
from games.mafia.WaitMessageSettings import WaitMessageSettings, WAIT_MESSAGE_PROCESSOR

if TYPE_CHECKING:
    from games.mafia.MafiaWorker import MafiaWorker
from games.mafia.logic.MafiaAction import MafiaAction, WaitBeforeNextAction, SendGlobalMessage, SendWhisperMessage, \
    WaitForAnswer, WaitForAnswerFromMany, StartNewNight, LockingMafiaAction, StartNewDay
from utils.Utils import MutableInt, CALLBACK_FUNCTION

if TYPE_CHECKING:
    MAFIA_ACTION_CALLBACK = Callable[[MafiaAction, MafiaWorker], None]
    MAFIA_LOCKING_ACTION_CALLBACK = Callable[[LockingMafiaAction, MafiaWorker], None]


def waitBeforeNextAction(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, WaitBeforeNextAction):
        _action: WaitBeforeNextAction = action

        _action.startWait()
        mafiaWorker.game.currentLockingAction = _action


def sendGlobalMessage(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, SendGlobalMessage):
        mafiaWorker.globalMessage(action.msg)


def sendWhisperMessage(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, SendWhisperMessage):
        mafiaWorker.whisperMessage(action.msg, action.receiver)


def waitForAnswer(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, WaitForAnswer):
        def onAnswerReceivedAndUnlockNextAction(msg: ChatMessage) -> bool:
            endWait = _action.onAnswerReceived(msg)
            if endWait:
                mafiaWorker.game.currentLockingAction = None
            return endWait

        def onAnswerNotReceivedAndUnlockNextAction() -> None:
            _action.onAnswerNotReceived()
            mafiaWorker.game.currentLockingAction = None

        _action: WaitForAnswer = action

        mafiaWorker.game.currentLockingAction = _action
        wms = WaitMessageSettings(_action.timeoutSecs, onAnswerReceivedAndUnlockNextAction,
                                  onAnswerNotReceivedAndUnlockNextAction)
        mafiaWorker.waitForAnswer(_action.desiredSender, wms)


def waitForAnswerFromMany(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, WaitForAnswerFromMany):
        _action: WaitForAnswerFromMany = action

        mafiaWorker.game.currentLockingAction = _action

        answers: dict[str, Optional[ChatMessage]] = {}

        lock = Lock()
        # Количество ответов, которое мы ожидаем:
        answersNeeded: MutableInt = MutableInt(len(_action.desiredSenders))

        def getAddAnswerConsumer(player: str) -> WAIT_MESSAGE_PROCESSOR:
            def wrapper(msg: ChatMessage) -> bool:
                if _action.onAnswerValidator is not None and not _action.onAnswerValidator(msg):
                    return False  # Если ответ не прошёл валидацию, продолжаем ждать ответа
                answers[player] = msg
                with lock:
                    answersNeeded.value -= 1
                return True

            return wrapper

        def getAddNotAnsweredCallback(player: str) -> CALLBACK_FUNCTION:
            def wrapper() -> None:
                if _action.onEachAnswerTimeout is not None:
                    _action.onEachAnswerTimeout(player)
                answers[player] = None
                with lock:
                    answersNeeded.value -= 1

            return wrapper

        for desiredSender in _action.desiredSenders:
            wms = WaitMessageSettings(_action.timeoutSecs, getAddAnswerConsumer(desiredSender),
                                      getAddNotAnsweredCallback(desiredSender))
            mafiaWorker.waitForAnswer(desiredSender, wms)

        def waitForAllAnswers() -> None:
            while True:
                sleep(0.5)
                with lock:
                    if answersNeeded.value > 0:
                        continue

                # Когда получили все ответы:
                mafiaWorker.game.currentLockingAction = None
                return _action.onAnswers(answers)

        thread = Thread(target=waitForAllAnswers, daemon=True)
        thread.start()


def startNewNight(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, StartNewNight):
        _action: StartNewNight = action

        mafiaWorker.game.nextNight()


def startNewDay(action: MafiaAction, mafiaWorker: MafiaWorker):
    if isinstance(action, StartNewDay):
        _action: StartNewDay = action

        mafiaWorker.game.nextDay()


ACTION_TYPE_TO_WORKER_ACTION: dict[Type[MafiaAction], MAFIA_ACTION_CALLBACK] = {
    WaitBeforeNextAction: waitBeforeNextAction,
    SendGlobalMessage: sendGlobalMessage,
    SendWhisperMessage: sendWhisperMessage,
    WaitForAnswer: waitForAnswer,
    WaitForAnswerFromMany: waitForAnswerFromMany,
    StartNewNight: startNewNight,
    StartNewDay: startNewDay
}


def waitBeforeNextActionLockUpdate(action: MafiaAction, mafiaWorker: MafiaWorker) -> None:
    if isinstance(action, WaitBeforeNextAction):
        _action: WaitBeforeNextAction = action

        if _action.isWaitEnded():
            mafiaWorker.game.currentLockingAction = None
            if _action.onTimeoutEnd is not None:
                _action.onTimeoutEnd()


def waitForAnswerLockUpdate(action: MafiaAction, mafiaWorker: MafiaWorker) -> None:
    pass


def waitForAnswerFromManyLockUpdate(action: MafiaAction, mafiaWorker: MafiaWorker) -> None:
    pass


ACTION_TYPE_TO_LOCKED_UPDATE_ACTION: dict[Type[LockingMafiaAction], MAFIA_LOCKING_ACTION_CALLBACK] = {
    WaitBeforeNextAction: waitBeforeNextActionLockUpdate,
    WaitForAnswer: waitForAnswerLockUpdate,
    WaitForAnswerFromMany: waitForAnswerFromManyLockUpdate,
}
