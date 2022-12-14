from __future__ import annotations

from games.mafia.logic.MafiaPlayer import MafiaPlayer


class MafiaState:
    players: list[MafiaPlayer]
    ended: bool
    night: bool
    dayNumber: int

    def __init__(self, players: list[MafiaPlayer]) -> None:
        self.ended = False
        self.players = players
        self.night = True
        self.dayNumber = 0

    def nextDay(self):
        self.night = False
        self.dayNumber += 1

    def nextNight(self):
        self.night = True

    def getAllAlive(self) -> list[MafiaPlayer]:
        return [player for player in self.players if player.alive]

    def getAllAliveNicknames(self) -> list[str]:
        return [player.nick for player in self.players if player.alive]
