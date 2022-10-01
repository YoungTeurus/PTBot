from games.mafia.logic.MafiaAction import SendWhisperMessage, WaitBeforeNextAction, SendGlobalMessage, MafiaAction
from games.mafia.logic.MafiaPlayer import MafiaPlayer
from games.mafia.logic.MafiaPlayerDistribution import PLAYABLE_CONFIGURATIONS
from games.mafia.logic.MafiaRolesDefinitions import MAFIA
from games.mafia.logic.MafiaState import MafiaState
from utils.ConsoleProvider import CONSOLE
from utils.RandUtils import randPopFromArr


class MafiaGame:
    state: MafiaState
    actionQueue: list[MafiaAction]

    def __init__(self, playersNames: list[str]):
        players = self.__makePlayers(playersNames)
        self.state = MafiaState(players)
        CONSOLE.print("Game is ready, players = '{}'".format(self.state.players))
        self.actionQueue = []

    @staticmethod
    def __makePlayers(playersNames: list[str]) -> list[MafiaPlayer]:
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
        actions: list[MafiaAction] = []

        for player in self.state.players:
            actions.append(
                SendWhisperMessage("{}, ваша роль - {}".format(player.nick, player.role.name), player.nick))

        self.actionQueue.extend(actions)

    def __nightZeroMafiaMeeting(self):
        actions: list[MafiaAction] = []

        mafiaNicknames: list[str] = []
        for player in self.state.players:
            if player.role == MAFIA:
                mafiaNicknames.append(player.nick)

        for mafia in mafiaNicknames:
            actions.append(SendWhisperMessage("Члены мафии: {}".format(", ".join(mafiaNicknames)), mafia))

        meetingDurationSecs = 30
        actions.append(SendGlobalMessage(
            "Город спит. Члены мафии в течении {} секунд знакомятся.".format(meetingDurationSecs)))
        actions.append(WaitBeforeNextAction(meetingDurationSecs))

        self.actionQueue.extend(actions)

    def __nextDay(self):
        self.state.nextDay()

        actions: list[MafiaAction] = []

        meetingDurationSecs = 60
        actions.append(SendGlobalMessage(
            "Город просыпается, у горожан есть 60 секунд на знакомство.".format(meetingDurationSecs)))
        actions.append(WaitBeforeNextAction(meetingDurationSecs))

        self.actionQueue.extend(actions)
