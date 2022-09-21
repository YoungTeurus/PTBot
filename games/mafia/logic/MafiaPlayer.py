from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from games.mafia.logic.MafiaRole import MafiaRole


class MafiaPlayer:
    nick: str
    role: MafiaRole
    alive: bool

    def __init__(self, nick: str, role: MafiaRole):
        self.nick = nick
        self.role = role
        self.alive = True

    def __str__(self) -> str:
        return "{} - {} - {}".format(self.nick, self.role.name, "жив" if self.alive else "мёртв")
