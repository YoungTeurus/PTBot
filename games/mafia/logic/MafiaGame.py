from typing import Optional

from games.mafia.logic.MafiaAction import SendWhisperMessage, WaitBeforeNextAction, SendGlobalMessage, MafiaAction, \
    StartNewNight, StartNewDay, NoStateMutationMafiaAction, LockingMafiaAction
from games.mafia.logic.MafiaPlayer import MafiaPlayer
from games.mafia.logic.MafiaPlayerDistribution import PLAYABLE_CONFIGURATIONS
from games.mafia.logic.MafiaProperties import DAY_TALKING_DURATION_SECS, FIRST_NIGHT_MAFIA_TALKING_DURATION_SECS
from games.mafia.logic.MafiaRoleActions import MafiaRoleActions
from games.mafia.logic.MafiaRolesDefinitions import MAFIA, NIGHT_ROLES_TURN_ORDER
from games.mafia.logic.MafiaState import MafiaState
from utils.ConsoleProvider import CONSOLE
from utils.RandUtils import randPopFromArr


class MafiaGame:
    state: MafiaState

    # Текущее длительное действие, завершения которого необходимо дождаться перед выполнением следующего действия из actionQueue
    currentLockingAction: Optional[LockingMafiaAction]

    # Действия, выполняемые по мере поступления и завершения предыдущего действия:
    actionQueue: list[MafiaAction]
    # Действия, выполняемые следующим утром:
    onNewDayStartActionQueue: list[MafiaAction]
    # Дейсвтия, выполянемые сразу же:
    immediateActionQueue: list[NoStateMutationMafiaAction]

    def __init__(self, playersNames: list[str]):
        players = self.__makePlayers(playersNames)
        self.state = MafiaState(players)
        CONSOLE.print("Game is ready, players = '{}'".format(self.state.players))

        self.currentLockingAction = None
        self.actionQueue = []
        self.onNewDayStartActionQueue = []
        self.immediateActionQueue = []

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

        actions.append(SendGlobalMessage(
            "Город спит. Члены мафии в течении {} секунд знакомятся.".format(FIRST_NIGHT_MAFIA_TALKING_DURATION_SECS)))
        actions.append(WaitBeforeNextAction(FIRST_NIGHT_MAFIA_TALKING_DURATION_SECS))

        self.actionQueue.extend(actions)

    def __nextDay(self):
        self.state.nextDay()

        actions: list[MafiaAction] = []

        actions.append(SendGlobalMessage(
            "Город просыпается, у горожан есть {} секунд на знакомство.".format(DAY_TALKING_DURATION_SECS)))
        actions.append(WaitBeforeNextAction(DAY_TALKING_DURATION_SECS))
        actions.append(StartNewNight())

        self.actionQueue.extend(actions)

    def nextNight(self):
        self.state.nextNight()

        actions: list[MafiaAction] = []

        actions.append(SendGlobalMessage("Город засыпает."))

        # Для всех ночных ролей выполнить их onNightStart действие:
        # В порядке действия ночных ролей выполнить их onNightTurn действие:
        for role in NIGHT_ROLES_TURN_ORDER:
            actions.extend(MafiaRoleActions.onNightTurn(role, self))
        # Для всех ночных ролей выполнить их onNightEnd действие:

        # После выполнения всех действий - начать новый день
        actions.append(StartNewDay())

        self.actionQueue.extend(actions)
