from collections import Callable
from typing import Optional

from utils.ConsoleProvider import CONSOLE
from utils.Utils import CALLBACK_FUNCTION

# (players) => None
ON_START_CALLBACK = ON_CLOSE_CALLBACK = Callable[[list[str]], None]
# (quited_player, remained_players) => None
ON_PLAYER_ENTER_CALLBACK = ON_PLAYER_LEAVE_CALLBACK = Callable[[str, list[str]], None]


class PlayerCountLobbySettings:
    minPlayersForStart: int
    onTooLittlePeopleToStart: Optional[CALLBACK_FUNCTION]
    maxPlayersInLobby: int
    onTooManyPeopleInLobby: Optional[CALLBACK_FUNCTION]

    # TODO: init


class Lobby:
    playerCountSettings: PlayerCountLobbySettings

    players: list[str]
    actionOnStart: ON_START_CALLBACK
    actionOnPlayerEnter: Optional[ON_PLAYER_ENTER_CALLBACK]
    actionOnPlayerLeave: Optional[ON_PLAYER_LEAVE_CALLBACK]
    actionOnPlayerLeaveNotPresent: Optional[ON_PLAYER_LEAVE_CALLBACK]
    actionOnClose: Optional[ON_CLOSE_CALLBACK]

    open: bool

    def __init__(self, settings: PlayerCountLobbySettings, actionOnStart: ON_START_CALLBACK,
                 actionOnPlayerEnter: ON_PLAYER_ENTER_CALLBACK = None,
                 actionOnPlayerLeave: ON_PLAYER_LEAVE_CALLBACK = None,
                 actionOnPlayerLeaveNotPresent: ON_PLAYER_LEAVE_CALLBACK = None,
                 actionOnClose: ON_CLOSE_CALLBACK = None):
        self.playerCountSettings = settings
        self.players = []
        self.actionOnStart = actionOnStart
        self.actionOnPlayerEnter = actionOnPlayerEnter
        self.actionOnPlayerLeave = actionOnPlayerLeave
        self.actionOnPlayerLeaveNotPresent = actionOnPlayerLeaveNotPresent
        self.actionOnClose = actionOnClose

        self.open = True

    def start(self) -> None:
        if (playerCount := len(self.players)) < self.playerCountSettings.minPlayersForStart:
            CONSOLE.print("There was too few players ({}) in lobby to start need at least ({})"
                          .format(playerCount, self.playerCountSettings.minPlayersForStart))
            if self.playerCountSettings.onTooLittlePeopleToStart is not None:
                self.playerCountSettings.onTooLittlePeopleToStart()
        CONSOLE.print("Starting from lobby with players: {}".format(self.players))
        self.actionOnStart(self.players)

    def enter(self, player: str) -> None:
        if (playerCount := len(self.players)) >= self.playerCountSettings.maxPlayersInLobby:
            CONSOLE.print("There was too many players ({}) for new ('{}') to join in"
                          .format(playerCount, player))
            if self.playerCountSettings.onTooManyPeopleInLobby is not None:
                self.playerCountSettings.onTooManyPeopleInLobby()
        CONSOLE.print("Adding ('{}') as a new player in lobby ({}/{})"
                      .format(player, playerCount, self.playerCountSettings.maxPlayersInLobby))

    def leave(self, player: str) -> None:
        if player not in self.players:
            CONSOLE.print("Player ('{}') was not in lobby to leave it".format(player))
            if self.actionOnPlayerLeaveNotPresent is not None:
                self.actionOnPlayerLeaveNotPresent(player, self.players)
        self.players.remove(player)
        CONSOLE.print("Player ('{}') left the lobby ({}/{})".format(player, len(self.players),
                                                                    self.playerCountSettings.maxPlayersInLobby))
        if self.actionOnPlayerLeave is not None:
            self.actionOnPlayerLeave(player, self.players)

    def close(self) -> None:
        CONSOLE.print("Closing lobby with players: {}".format(self.players))
        if self.actionOnClose is not None:
            self.actionOnClose(self.players)
        self.players.clear()
        self.open = False
