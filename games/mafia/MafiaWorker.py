from __future__ import annotations

import time
from typing import Callable

from activities.BaseActivity import BaseActivity
from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from games.mafia.MafiaActionTranformer import ACTION_TYPE_TO_WORKER_ACTION
from games.mafia.WaitMessageSettings import WaitMessageSettings
from games.mafia.logic.MafiaAction import MafiaAction
from games.mafia.logic.MafiaGame import MafiaGame
from modules.base.Command import Command
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenChatObserver


class MafiaWorker(OutputtingCommandDrivenChatObserver, BaseActivity):
    game: MafiaGame

    # (player_name) => (startWaitTime, timeout, onCommand, onTimeout)
    waitingForAnswers: dict[str, WaitMessageSettings]
    # Задержка перед следующим action:
    waitBeforeNextActionSecs: float
    __lastUpdateTime: float

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory, game: MafiaGame):
        super().__init__(csqs, ocmf, acceptNonCommandInputWithPrefix=True)
        self.game = game
        self.waitingForAnswers = {}
        self.waitBeforeNextActionSecs = 0
        self.__lastUpdateTime = time.time()

        self.game.start()

    def waitForAnswer(self, desiredSender: str, wms: WaitMessageSettings):
        if desiredSender in self.waitingForAnswers:
            raise RuntimeError("Already waiting for input from user '{}'".format(desiredSender))
        self.waitingForAnswers[desiredSender] = wms

    def onNonCommandInput(self, msg: ChatMessage, hasPrefix: bool) -> NotifyAction:
        if hasPrefix:
            self.__checkAnswerForWait(msg)
        # else:
        #     pass
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER

    def update(self) -> None:
        curTime: float = time.time()
        self.__checkWaitForAnswersTimeouts(curTime)
        if self.waitBeforeNextActionSecs > 0:
            self.waitBeforeNextActionSecs -= (curTime - self.__lastUpdateTime)
        elif len(self.game.actionQueue) > 0:
            action: MafiaAction = self.game.actionQueue.pop(0)
            ACTION_TYPE_TO_WORKER_ACTION[action.__class__](action, self)
        self.__lastUpdateTime = curTime

    def _getInitialCommands(self) -> list[Command]:
        return []

    def __checkWaitForAnswersTimeouts(self, curTime: float) -> None:
        for playerName in self.waitingForAnswers:
            waitTuple = self.waitingForAnswers[playerName]
            if waitTuple.startWaitTime + waitTuple.timeoutSecs > curTime:
                waitTuple.onTimeout()

    def endObserving(self) -> None:
        self.selfRemove()

    def __checkAnswerForWait(self, msg: ChatMessage) -> None:
        removeWaitKeys: list[str] = []
        if (sender := msg.sender) in self.waitingForAnswers:
            removeWait = self.waitingForAnswers[sender].onCommand(msg)
            if removeWait:
                removeWaitKeys.append(sender)
        for key in removeWaitKeys:
            self.waitingForAnswers.pop(key)


MAFIA_WORKER_CONSUMER = Callable[[MafiaWorker], None]
