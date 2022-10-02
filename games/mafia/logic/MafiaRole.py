class MafiaTeam:
    name: str


class MafiaRole:
    name: str
    team: MafiaTeam

    def __str__(self):
        return "<MafiaRole - {}>".format(self.name)


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
