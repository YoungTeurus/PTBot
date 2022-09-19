from typing import Optional, Callable

from utils.ConsoleProvider import CONSOLE
from utils.Utils import CALLBACK_FUNCTION

# (players) => None
ON_START_CALLBACK = ON_CLOSE_CALLBACK = Callable[[list[str]], None]
# (quited_player, remained_players) => None
ON_PLAYER_JOIN_CALLBACK = ON_PLAYER_LEAVE_CALLBACK = Callable[[str, list[str]], None]


class PlayerLobbySettings:
    minPlayersForStart: int
    onTooLittlePeopleToStart: Optional[CALLBACK_FUNCTION]
    maxPlayersInLobby: int
    onTooManyPeopleInLobby: Optional[CALLBACK_FUNCTION]

    onPlayerJoin: Optional[ON_PLAYER_JOIN_CALLBACK]
    onPlayerJoinAlreadyIn: Optional[ON_PLAYER_JOIN_CALLBACK]
    onPlayerLeave: Optional[ON_PLAYER_LEAVE_CALLBACK]
    onPlayerLeaveNotPresent: Optional[ON_PLAYER_LEAVE_CALLBACK]

    def __init__(self, minPlayersForStart: int,
                 maxPlayersInLobby: int,
                 onTooLittlePeopleToStart: Optional[CALLBACK_FUNCTION] = None,
                 onTooManyPeopleInLobby: Optional[CALLBACK_FUNCTION] = None,
                 onPlayerJoin: Optional[ON_PLAYER_JOIN_CALLBACK] = None,
                 onPlayerJoinAlreadyIn: Optional[ON_PLAYER_JOIN_CALLBACK] = None,
                 onPlayerLeave: Optional[ON_PLAYER_LEAVE_CALLBACK] = None,
                 onPlayerLeaveNotPresent: Optional[ON_PLAYER_LEAVE_CALLBACK] = None):
        self.minPlayersForStart = minPlayersForStart
        self.onTooLittlePeopleToStart = onTooLittlePeopleToStart
        self.maxPlayersInLobby = maxPlayersInLobby
        self.onTooManyPeopleInLobby = onTooManyPeopleInLobby
        self.onPlayerJoin = onPlayerJoin
        self.onPlayerJoinAlreadyIn = onPlayerJoinAlreadyIn
        self.onPlayerLeave = onPlayerLeave
        self.onPlayerLeaveNotPresent = onPlayerLeaveNotPresent


class Lobby:
    playerSettings: PlayerLobbySettings

    players: list[str]
    actionOnStart: ON_START_CALLBACK
    actionOnClose: Optional[ON_CLOSE_CALLBACK]

    open: bool

    def __init__(self, playerSettings: PlayerLobbySettings,
                 actionOnStart: ON_START_CALLBACK,
                 actionOnClose: ON_CLOSE_CALLBACK = None):
        self.playerSettings = playerSettings
        self.players = []
        self.actionOnStart = actionOnStart
        self.actionOnClose = actionOnClose

        self.open = True

    def start(self) -> None:
        if (playerCount := len(self.players)) < self.playerSettings.minPlayersForStart:
            CONSOLE.print("There was too few players ({}) in lobby to start need at least ({})"
                          .format(playerCount, self.playerSettings.minPlayersForStart))
            if self.playerSettings.onTooLittlePeopleToStart is not None:
                self.playerSettings.onTooLittlePeopleToStart()
            return
        CONSOLE.print("Starting from lobby with players: {}".format(self.players))
        self.actionOnStart(self.players)

    def join(self, player: str) -> None:
        if (playerCount := len(self.players)) >= self.playerSettings.maxPlayersInLobby:
            CONSOLE.print("There was too many players ({}) for new ('{}') to join in"
                          .format(playerCount, player))
            if self.playerSettings.onTooManyPeopleInLobby is not None:
                self.playerSettings.onTooManyPeopleInLobby()
            return

        if player in self.players:
            CONSOLE.print("Player ('{}') was already in lobby".format(player))
            if self.playerSettings.onPlayerJoinAlreadyIn is not None:
                self.playerSettings.onPlayerJoinAlreadyIn(player, self.players)
            return

        self.players.append(player)
        CONSOLE.print("'{}' joined the lobby ({}/{})"
                      .format(player, len(self.players), self.playerSettings.maxPlayersInLobby))

        if self.playerSettings.onPlayerJoin is not None:
            self.playerSettings.onPlayerJoin(player, self.players)

    def leave(self, player: str) -> None:
        if player not in self.players:
            CONSOLE.print("Player ('{}') was not in lobby to leave it".format(player))
            if self.playerSettings.onPlayerLeaveNotPresent is not None:
                self.playerSettings.onPlayerLeaveNotPresent(player, self.players)
            return

        self.players.remove(player)
        CONSOLE.print("'{}' left the lobby ({}/{})".format(player, len(self.players),
                                                                    self.playerSettings.maxPlayersInLobby))
        if self.playerSettings.onPlayerLeave is not None:
            self.playerSettings.onPlayerLeave(player, self.players)

    def close(self) -> None:
        CONSOLE.print("Closing lobby with players: {}".format(self.players))
        if self.actionOnClose is not None:
            self.actionOnClose(self.players)
        self.players.clear()
        self.open = False
