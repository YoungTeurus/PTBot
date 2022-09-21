from games.mafia.logic.MafiaPlayer import MafiaPlayer
from games.mafia.logic.MafiaPlayerDistribution import PLAYABLE_CONFIGURATIONS
from games.mafia.logic.MafiaState import MafiaState
from utils.ConsoleProvider import CONSOLE
from utils.RandUtils import randPopFromArr


class MafiaGame:
    state: MafiaState

    def __init__(self, playersNames: list[str]):
        players = self.__makePlayers(playersNames)
        self.state = MafiaState(players)
        CONSOLE.print("Game is ready, players = '{}'".format(self.state.players))

    def __makePlayers(self, playersNames: list[str]) -> list[MafiaPlayer]:
        rolesToDistribute = PLAYABLE_CONFIGURATIONS[len(playersNames)]()

        players = []
        for name in playersNames:
            chosenRole = randPopFromArr(rolesToDistribute)
            players.append(MafiaPlayer(name, chosenRole))

        return players

    def start(self) -> None:
        self.__sendRolesToPlayers()
        self.__nightZeroMafiaMeeting()
        self.__nextDay()

    def __sendRolesToPlayers(self):
        pass

    def __nightZeroMafiaMeeting(self):
        pass

    def __nextDay(self):
        pass
