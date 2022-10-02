import random
from typing import Optional, Callable, TYPE_CHECKING

from chat.ChatMessage import ChatMessage
from games.mafia.logic.MafiaAction import MafiaAction, SendGlobalMessage, SendWhisperMessage, WaitForAnswerFromMany, \
    ANSWERS_DICT, KillPlayer, WaitBeforeNextAction
from games.mafia.logic.MafiaProperties import NIGHT_TURN_DURATIONS_SECS
from utils.ConsoleProvider import CONSOLE

if TYPE_CHECKING:
    from games.mafia.logic.MafiaGame import MafiaGame
from games.mafia.logic.MafiaRole import MafiaRole
from games.mafia.logic.MafiaRolesDefinitions import MAFIA, COMMISSAR
from properties import COMMAND_PREFIX
from utils.ArgsDevider import splitArgs
from utils.Utils import dictUpdate, dictMostCommon


def checkIfValidVictim(game: 'MafiaGame') -> Callable[[ChatMessage], bool]:
    def ifNamePresent(name: str, game: 'MafiaGame') -> bool:
        for player in game.state.players:
            if player.nick == name:
                return True
        return False

    def wrapper(msg: ChatMessage) -> bool:
        bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
        args = splitArgs(bodyWithoutPrefix)
        if len(args) == 0:
            game.immediateActionQueue.append(SendWhisperMessage("В сообщении не найдено имя жертвы!", msg.sender))
            return False
        victimName = args[0]
        if not ifNamePresent(victimName, game):
            game.immediateActionQueue.append(
                SendWhisperMessage("Имя '{}' не найдено среди имён игроков".format(victimName), msg.sender))
            return False
        return True

    return wrapper


def getVictimName(msg: ChatMessage) -> str:
    bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
    args = splitArgs(bodyWithoutPrefix)
    return args[0]


def onAcceptedVictimAnswer(game: 'MafiaGame') -> Callable[[ChatMessage], bool]:
    def wrapper(msg: ChatMessage) -> bool:
        victim = getVictimName(msg)
        game.immediateActionQueue.append(SendWhisperMessage("Игрок {} выбран в качестве жертвы".format(victim), msg.sender))
        return True

    return wrapper


def mafiaOnNightTurn(game: 'MafiaGame') -> list[MafiaAction]:
    turnDurationSecs = NIGHT_TURN_DURATIONS_SECS.MAFIA

    def countMafiaVotes(votes: ANSWERS_DICT) -> None:
        game.immediateActionQueue.append(SendGlobalMessage("Мафия сделала свой выбор..."))

        # player_nick => number_of_votes
        targetsToShots: dict[str, int] = {}

        for mafia in votes:
            vote: Optional[ChatMessage] = votes[mafia]
            if vote is None:
                continue
            victimName: str = getVictimName(vote)
            dictUpdate(targetsToShots, victimName, lambda k, v: 1 if v is None else v + 1)

        CONSOLE.print("Голоса мафии: {}".format(targetsToShots))

        if len(targetsToShots) == 0:
            CONSOLE.print("Цель не была выбрана")
            game.onNewDayStartActionQueue.append(SendGlobalMessage("Мафия не смогла определиться с целью для стрельбы."))
            return
        mostCommonNames: list[str] = dictMostCommon(targetsToShots)
        realVictimName: str = random.choice(mostCommonNames)
        CONSOLE.print("Цель мафии - {}".format(realVictimName))
        game.onNewDayStartActionQueue.append(KillPlayer(realVictimName, "Убит мафией"))

    actions: list[MafiaAction] = []

    actions.append(SendGlobalMessage("Просыпается мафия. У неё есть {} секунд, чтобы решить, кто умрёт сегодня ночью."
                                     .format(turnDurationSecs)))

    mafias: list[str] = []

    for player in game.state.players:
        if player.role == MAFIA:
            mafias.append(player.nick)
            actions.append(
                SendWhisperMessage("{}, чтобы выбрать жертву, отправь его имя как команду, например, '{}{}'".format(
                    player.nick, COMMAND_PREFIX, player.nick
                ), player.nick))

    actions.append(WaitForAnswerFromMany(mafias, turnDurationSecs, countMafiaVotes,
                                         checkIfValidVictim(game), onAcceptedVictimAnswer(game)))

    return actions


def commissarOnNightTurn(game: 'MafiaGame') -> list[MafiaAction]:
    turnDurationSecs = NIGHT_TURN_DURATIONS_SECS.COMMISSAR

    actions: list[MafiaAction] = []

    actions.append(SendGlobalMessage("Просыпается комиссар. У него есть {} секунд, чтобы решить, кого он проверит."
                                     .format(turnDurationSecs)))
    actions.append(WaitBeforeNextAction(turnDurationSecs))

    return actions


ROLE_ON_NIGHT_TURN = {
    MAFIA: mafiaOnNightTurn,
    COMMISSAR: commissarOnNightTurn
}


class MafiaRoleActions:
    @staticmethod
    def onGameStart(role: MafiaRole, game: 'MafiaGame') -> list[MafiaAction]:
        pass

    @staticmethod
    def onDayStart(role: MafiaRole, game: 'MafiaGame') -> list[MafiaAction]:
        pass

    @staticmethod
    def onDayEnd(role: MafiaRole, game: 'MafiaGame') -> list[MafiaAction]:
        pass

    @staticmethod
    def onNightStart(role: MafiaRole, game: 'MafiaGame') -> list[MafiaAction]:
        pass

    @staticmethod
    def onNightTurn(role: MafiaRole, game: 'MafiaGame') -> list[MafiaAction]:
        return ROLE_ON_NIGHT_TURN[role](game)

    @staticmethod
    def onNightEnd(role: MafiaRole, game: 'MafiaGame') -> list[MafiaAction]:
        pass

    @staticmethod
    def onDeath(role: MafiaRole, game: 'MafiaGame') -> list[MafiaAction]:
        pass

    @staticmethod
    def onGameEnd(role: MafiaRole, game: 'MafiaGame') -> list[MafiaAction]:
        pass
