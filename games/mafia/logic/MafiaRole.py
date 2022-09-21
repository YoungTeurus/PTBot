from collections import Callable

from games.mafia.logic.MafiaPlayer import MafiaPlayer
from games.mafia.logic.MafiaState import MafiaState
# (player, game_state) => None
from utils.Utils import groupBy

# (acting_player, state) => None
MAFIA_ROLE_ACTION = Callable[[MafiaPlayer, MafiaState], None]


class MafiaTeam:
    name: str

    onTeamMemberDead: MAFIA_ROLE_ACTION


CIVILIANS = MafiaTeam()
CIVILIANS.name = "Мирные жители"

MAFIAS = MafiaTeam()
MAFIAS.name = "Члены мафии"

ALL_TEAMS = [CIVILIANS, MAFIAS]


def haveTeamWonByMajority(checkingTeam: MafiaTeam, state: MafiaState, strictMajority: bool) -> bool:
    def getPlayerRoleGroup(player: MafiaPlayer) -> MafiaTeam:
        return player.role.team

    teamCount = groupBy(state.players, getPlayerRoleGroup)
    for team in teamCount:
        if team != checkingTeam:
            if strictMajority:
                if len(teamCount[team]) >= len(teamCount[checkingTeam]):
                    return False
            else:
                if len(teamCount[team]) > len(teamCount[checkingTeam]):
                    return False
    return True


def haveMafiaWon(state: MafiaState):
    return haveTeamWonByMajority(MAFIAS, state, False)


def haveCiviliansWon(state: MafiaState):
    return haveTeamWonByMajority(CIVILIANS, state, True)


def addTeamWonEvent(team: MafiaTeam, state: MafiaState) -> None:
    state.actionQueue.append(lambda: print("{} победили!".format(team.name)))


CIVILIANS.onTeamMemberDead = (
    lambda killed, state: addTeamWonEvent(MAFIAS, state) if haveMafiaWon(killed) else None)
MAFIAS.onTeamMemberDead = (
    lambda killed, state: addTeamWonEvent(CIVILIANS, state) if haveCiviliansWon(killed) else None)


class MafiaRole:
    name: str
    team: MafiaTeam

    onGameStart: MAFIA_ROLE_ACTION

    onDayStart: MAFIA_ROLE_ACTION
    onDayEnd: MAFIA_ROLE_ACTION
    onNightStart: MAFIA_ROLE_ACTION
    onNightTurn: MAFIA_ROLE_ACTION
    onNightEnd: MAFIA_ROLE_ACTION

    onDeath: MAFIA_ROLE_ACTION

    onGameEnd: MAFIA_ROLE_ACTION


CIVILIAN = MafiaRole()
CIVILIAN.name = "Мирный"
CIVILIAN.team = CIVILIANS
CIVILIAN.onDeath = lambda player, state: CIVILIAN.team.onTeamMemberDead(player, state)

COMMISSAR = MafiaRole()
COMMISSAR.name = "Комиссар"
COMMISSAR.team = CIVILIANS
COMMISSAR.onDeath = lambda player, state: COMMISSAR.team.onTeamMemberDead(player, state)
COMMISSAR.onNightTurn = lambda: None  # TODO

MAFIA = MafiaRole()
MAFIA.name = "Мафия"
MAFIA.team = MAFIAS
MAFIA.onDeath = lambda player, state: MAFIA.team.onTeamMemberDead(player, state)
MAFIA.onNightTurn = lambda: None  # TODO

ALL_ROLES: list[MafiaRole] = [CIVILIAN, MAFIA, COMMISSAR]

NIGHT_ROLES_TURN_ORDER: list[MafiaRole] = [MAFIA, COMMISSAR]
