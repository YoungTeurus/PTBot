# from games.mafia.logic.Utils import MAFIA_ROLE_ACTION


class MafiaTeam:
    name: str
    # onTeamMemberDead: MAFIA_ROLE_ACTION


class MafiaRole:
    name: str
    team: MafiaTeam

    # onGameStart: MAFIA_ROLE_ACTION
    #
    # onDayStart: MAFIA_ROLE_ACTION
    # onDayEnd: MAFIA_ROLE_ACTION
    # onNightStart: MAFIA_ROLE_ACTION
    # onNightTurn: MAFIA_ROLE_ACTION
    # onNightEnd: MAFIA_ROLE_ACTION
    #
    # onDeath: MAFIA_ROLE_ACTION
    #
    # onGameEnd: MAFIA_ROLE_ACTION
