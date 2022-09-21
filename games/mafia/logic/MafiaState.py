from __future__ import annotations
from collections import Callable

from games.mafia.logic.MafiaPlayer import MafiaPlayer


class MafiaState:
    players: list[MafiaPlayer]
    actionQueue: list[Callable[[MafiaState], None]]
    ended: bool

    night: bool
    nightNumber: int

    def __init__(self, players: list[MafiaPlayer]) -> None:
        self.ended = False
        self.players = players
        self.actionQueue = []
        self.night = True
        self.nightNumber = 0


MAFIA_STATE_CALLBACK = Callable[[MafiaState], None]
