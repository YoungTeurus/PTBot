from games.mafia.logic.MafiaRole import MafiaTeam, MafiaRole

# Teams:
CIVILIANS = MafiaTeam()
CIVILIANS.name = "Мирные жители"

MAFIAS = MafiaTeam()
MAFIAS.name = "Члены мафии"

ALL_TEAMS = [CIVILIANS, MAFIAS]

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
