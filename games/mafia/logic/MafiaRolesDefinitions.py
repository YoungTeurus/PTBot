from games.mafia.logic.MafiaRole import MafiaTeam, MafiaRole

# Teams:
CIVILIANS = MafiaTeam()
CIVILIANS.name = "Мирные жители"

MAFIAS = MafiaTeam()
MAFIAS.name = "Члены мафии"

ALL_TEAMS = [CIVILIANS, MAFIAS]

# def haveTeamWonByMajority(checkingTeam: MafiaTeam, state: MafiaState, strictMajority: bool) -> bool:
#     def getPlayerRoleGroup(player: MafiaPlayer) -> MafiaTeam:
#         return player.role.team
#
#     teamCount = groupBy(state.players, getPlayerRoleGroup)
#     for team in teamCount:
#         if team != checkingTeam:
#             if strictMajority:
#                 if len(teamCount[team]) >= len(teamCount[checkingTeam]):
#                     return False
#             else:
#                 if len(teamCount[team]) > len(teamCount[checkingTeam]):
#                     return False
#     return True
#
#
# def haveMafiaWon(state: MafiaState):
#     return haveTeamWonByMajority(MAFIAS, state, False)
#
#
# def haveCiviliansWon(state: MafiaState):
#     return haveTeamWonByMajority(CIVILIANS, state, True)
#
#
# def addTeamWonEvent(team: MafiaTeam, game: MafiaGame) -> None:
#     game.actionQueue.append(SendGlobalMessage("{} победили!".format(team.name)))
#
#
# def civiliansOnTeamMemberDead(game: MafiaGame) -> None:
#     if haveMafiaWon(game.state):
#         addTeamWonEvent(MAFIAS, game)
#
#
# def mafiasOnTeamMemberDead(game: MafiaGame) -> None:
#     if haveCiviliansWon(game.state):
#         addTeamWonEvent(CIVILIANS, game)
#
#
# CIVILIANS.onTeamMemberDead = civiliansOnTeamMemberDead
# MAFIAS.onTeamMemberDead = mafiasOnTeamMemberDead

# Roles:
CIVILIAN = MafiaRole()
CIVILIAN.name = "Мирный"
CIVILIAN.team = CIVILIANS

COMMISSAR = MafiaRole()
COMMISSAR.name = "Комиссар"
COMMISSAR.team = CIVILIANS

MAFIA = MafiaRole()
MAFIA.name = "Мафия"
MAFIA.team = MAFIAS

ALL_ROLES: list[MafiaRole] = [CIVILIAN, MAFIA, COMMISSAR]

NIGHT_ROLES_TURN_ORDER: list[MafiaRole] = [MAFIA, COMMISSAR]
