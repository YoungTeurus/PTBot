import random
from typing import Optional, Callable, TYPE_CHECKING

from chat.ChatMessage import ChatMessage
from games.mafia.logic.MafiaAction import MafiaAction, SendGlobalMessage, SendWhisperMessage, WaitForAnswerFromMany, \
    ANSWERS_DICT, KillPlayer, WaitBeforeNextAction, WaitForAnswer
from games.mafia.logic.MafiaPlayer import MafiaPlayer
from games.mafia.logic.MafiaProperties import NIGHT_TURN_DURATIONS_SECS
from games.mafia.logic.Utils import countOnlyNotNoneAnswers, VOTED_COUNT_DICT, extractFirstArg
from utils.ConsoleProvider import CONSOLE

if TYPE_CHECKING:
    from games.mafia.logic.MafiaGame import MafiaGame
from games.mafia.logic.MafiaRole import MafiaRole
from games.mafia.logic.MafiaRolesDefinitions import MAFIA, COMMISSAR
from properties import COMMAND_PREFIX
from utils.ArgsDevider import splitArgs
from utils.Utils import dictMostCommon


def checkIfValidVictim(game: 'MafiaGame') -> Callable[[ChatMessage], bool]:
    def wrapper(msg: ChatMessage) -> bool:
        bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
        args = splitArgs(bodyWithoutPrefix)
        if len(args) == 0:
            game.immediateActionQueue.append(SendWhisperMessage("В сообщении не найдено имя жертвы!", msg.sender))
            return False
        victimName = args[0]
        if victimName not in game.state.getAllAliveNicknames():
            game.immediateActionQueue.append(
                SendWhisperMessage("Имя '{}' не найдено среди имён живых игроков".format(victimName), msg.sender))
            return False
        game.immediateActionQueue.append(
            SendWhisperMessage("Игрок {} выбран в качестве жертвы".format(victimName), msg.sender))
        return True

    return wrapper


def onVictimAnswerTimeout(game: 'MafiaGame') -> Callable[[str], None]:
    def wrapper(player: str) -> None:
        game.immediateActionQueue.append(SendWhisperMessage("Вы не успели выбрать жертву.", player))

    return wrapper


def mafiaOnNightTurn(game: 'MafiaGame') -> list[MafiaAction]:
    turnDurationSecs = NIGHT_TURN_DURATIONS_SECS.MAFIA

    def countMafiaVotes(votes: ANSWERS_DICT) -> None:
        game.immediateActionQueue.append(SendGlobalMessage("Мафия сделала свой выбор..."))

        # player_nick => number_of_votes
        targetsToShots: VOTED_COUNT_DICT = countOnlyNotNoneAnswers(votes, extractFirstArg)

        CONSOLE.print("Голоса мафии: {}".format(targetsToShots))

        if len(targetsToShots) == 0:
            CONSOLE.print("Цель не была выбрана")
            game.actionQueue.append(
                SendGlobalMessage("Мафия не смогла определиться с целью для стрельбы."))
            return
        mostCommonNames: list[str] = dictMostCommon(targetsToShots)
        realVictimName: str = random.choice(mostCommonNames)
        CONSOLE.print("Цель мафии - {}".format(realVictimName))
        game.actionQueue.append(KillPlayer(realVictimName, "Убит мафией"))

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
                                         checkIfValidVictim(game), onVictimAnswerTimeout(game)))

    return actions


def getAliveCommissar(game: 'MafiaGame') -> Optional[MafiaPlayer]:
    for player in game.state.players:
        if player.role == COMMISSAR and player.alive:
            return player
    return None


def getPlayerRole(name: str, game: 'MafiaGame') -> MafiaRole:
    for player in game.state.players:
        if player.nick == name:
            return player.role
    raise RuntimeError("Player {} was not found".format(name))


def onCommissarMsg(game: 'MafiaGame') -> Callable[[ChatMessage], bool]:
    def wrapper(msg: ChatMessage) -> bool:
        bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
        args = splitArgs(bodyWithoutPrefix)
        if len(args) == 0:
            game.immediateActionQueue.append(SendWhisperMessage("В сообщении не найдено имя проверяемого!", msg.sender))
            return False
        checkingName = args[0]
        if checkingName not in game.state.getAllAliveNicknames():
            game.immediateActionQueue.append(
                SendWhisperMessage("Имя '{}' не найдено среди имён живых игроков".format(checkingName), msg.sender))
            return False
        if checkingName == msg.sender:
            game.immediateActionQueue.append(
                SendWhisperMessage("Вы не можете проверить самого себя", msg.sender))
            return False
        checkingNameRole: MafiaRole = getPlayerRole(checkingName, game)
        game.immediateActionQueue.append(
            SendWhisperMessage("Игрок {} - {}".format(checkingName, checkingNameRole.name), msg.sender))
        game.immediateActionQueue.append(SendGlobalMessage("Коммисар закончил свою проверку..."))
        return True

    return wrapper


def onCommissarMsgTimeout(game: 'MafiaGame') -> Callable[[str], None]:
    def wrapper(player: str) -> None:
        game.immediateActionQueue.append(SendWhisperMessage("Вы не успели выбрать проверяемого.", player))

    return wrapper


def commissarOnNightTurn(game: 'MafiaGame') -> list[MafiaAction]:
    turnDurationSecs = NIGHT_TURN_DURATIONS_SECS.COMMISSAR

    actions: list[MafiaAction] = []

    actions.append(SendGlobalMessage("Просыпается комиссар. У него есть {} секунд, чтобы решить, кого он проверит."
                                     .format(turnDurationSecs)))

    commissar: MafiaPlayer = getAliveCommissar(game)
    if commissar is not None:
        actions.append(
            SendWhisperMessage("{}, чтобы выбрать проверяемого, отправь его имя как команду, например, '{}{}'".format(
                commissar.nick, COMMAND_PREFIX, commissar.nick),
                commissar.nick))
        actions.append(
            WaitForAnswer(commissar.nick, turnDurationSecs, onCommissarMsg(game), onCommissarMsgTimeout(game)))
    else:
        # Если комиссар мёртв - просто ждём указанное время
        actions.append(WaitBeforeNextAction(turnDurationSecs,
                                            lambda: game.immediateActionQueue.append(
                                                SendGlobalMessage("Коммисар закончил свою проверку...")
                                            ))
                       )

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
