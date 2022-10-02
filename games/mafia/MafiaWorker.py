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

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory, game: MafiaGame):
        super().__init__(csqs, ocmf, acceptNonCommandInputWithPrefix=True)
        self.game = game
        self.waitingForAnswers = {}

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
        self.__checkWaitForAnswersTimeouts()

        while len(self.game.immediateActionQueue) > 0:
            immediateAction: MafiaAction = self.game.immediateActionQueue.pop(0)
            ACTION_TYPE_TO_WORKER_ACTION[immediateAction.__class__](immediateAction, self)

        if self.game.currentAction.finished():
            self.game.currentAction = self.game.actions.pop(0) if len(self.game.actions) > 0 else None
        if self.game.currentAction is not None:
            self.game.currentAction.act(self)

        # if (lockingAction := self.game.currentLockingAction) is not None:
        #     ACTION_TYPE_TO_LOCKED_UPDATE_ACTION[lockingAction.__class__](lockingAction, self)
        # elif len(self.game.actionQueue) > 0:
        #     action: MafiaAction = self.game.actionQueue.pop(0)
        #     ACTION_TYPE_TO_WORKER_ACTION[action.__class__](action, self)

    def _getInitialCommands(self) -> list[Command]:
        return []

    def __checkWaitForAnswersTimeouts(self) -> None:
        curTime: float = time.time()
        for playerName in self.waitingForAnswers:
            waitTuple = self.waitingForAnswers[playerName]
            if curTime > waitTuple.startWaitTime + waitTuple.timeoutSecs:
                waitTuple.onTimeout(playerName)

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
