from typing import Optional

from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from games.lobby.Lobby import Lobby, PlayerLobbySettings
from modules.base.Command import Command, CommandArg, ARGS_DICT, CHAT_MESSAGE_KEY
from modules.base.CommandDrivenChatObserver import ACTION_ON_COMMAND_ERROR_HANDLER
from modules.base.CommandProvider import CommandProvider
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenChatObserver
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import CONSOLE


class LobbyCreator(OutputtingCommandDrivenChatObserver, CommandProvider):
    bp: BotProperties

    lobby: Optional[Lobby]

    onlyAdminsCanJoin: bool
    bannedPlayers: list[str]

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory, bp: BotProperties,
                 actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER = None,
                 acceptNonCommandInputWithPrefix: bool = False):
        super().__init__(csqs, ocmf, actionOnCommandError, acceptNonCommandInputWithPrefix)
        self.bp = bp
        self.lobby = None

    def getConsoleCommands(self) -> list[Command]:
        pass

    def _getInitialCommands(self) -> list[Command]:
        return [
            Command("лобби", self.__lobby, optionalArgs=[CommandArg("onlyAdmins")]),
        ]

    def __onLobbyClosure(self) -> None:
        self.lobby = None
        self.__setCommandOnLobbyClose()

    def __setCommandOnLobbyClose(self) -> None:
        commandsToAdd = self._getInitialCommands()
        self.addCommands(commandsToAdd)
        commandsToRemove = ["настройка", "начать", "войти", "выйти", "выгнать", "игроки", "закрыть"]
        self.removeCommands(commandsToRemove)

    def __onLobbyCreation(self) -> None:
        self.bannedPlayers = []
        self.onlyAdminsCanJoin = True

        # TODO установка параметров лобби:
        settings = PlayerLobbySettings(2, 4)
        self.lobby = Lobby(settings,
                           (lambda players: CONSOLE.print("Lobby started with players {}".format(players))))
        self.__setCommandOnLobbyOpen()

    def __setCommandOnLobbyOpen(self) -> None:
        commandsToAdd = [
            Command("настройка", self.__settings, [CommandArg("name")], [CommandArg("value")]),
            Command("начать", self.__start),
            Command("войти", self.__join),
            Command("выйти", self.__leave),
            Command("выгнать", self.__kick, [CommandArg("name")], [CommandArg("doBan")]),
            Command("игроки", self.__players),
            Command("закрыть", self.__close),
        ]
        self.addCommands(commandsToAdd)
        commandsToRemove = ["лобби"]
        self.removeCommands(commandsToRemove)

    def __lobby(self, args: ARGS_DICT) -> None:
        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        if not msg.type.isSentByBotAdmin:
            self.globalMessage("{}, у тебя нет прав на создание лобби".format(msg.sender))
            return
        self.__onLobbyCreation()
        self.lobby.join(msg.sender)

        if "onlyAdmins" in args:
            self.onlyAdminsCanJoin = not (args["onlyAdmins"] == 'общее')

    def __settings(self, args: ARGS_DICT) -> None:
        if self.lobby is None:
            self.globalMessage("Лобби не было создано, но эта команда сработала? ЧТО-ТО НЕ ТАК!")
            return

        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        sender = msg.sender
        if self.onlyAdminsCanJoin and not msg.type.isSentByBotAdmin:
            self.globalMessage("{}, у тебя нет прав для изменения настроек лобби.".format(sender))
            return

        parameterName = args["name"]
        # TODO: Переделать на dict
        if parameterName == "админвход":
            if "value" not in args:
                self.whisperMessage(
                    "Текущее значение 'админвход' = {} (не было изменено)".format(self.onlyAdminsCanJoin), sender)
                return
            value = args["value"]
            if value == 'y':
                self.onlyAdminsCanJoin = True
            elif value == 'n':
                self.onlyAdminsCanJoin = False
            self.whisperMessage("Текущее значение 'админвход' = {}".format(self.onlyAdminsCanJoin), sender)

    def __start(self, args: ARGS_DICT) -> None:
        if self.lobby is None:
            self.globalMessage("Лобби не было создано, но эта команда сработала? ЧТО-ТО НЕ ТАК!")
            return

        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        sender = msg.sender
        if self.onlyAdminsCanJoin and not msg.type.isSentByBotAdmin:
            self.globalMessage("{}, у тебя нет прав для старта лобби.".format(sender))
            return

        if self.lobby.start():
            self.__onLobbyClosure()

    def __join(self, args: ARGS_DICT) -> None:
        if self.lobby is None:
            self.globalMessage("Лобби не было создано, но эта команда сработала? ЧТО-ТО НЕ ТАК!")
            return

        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        sender = msg.sender
        if self.onlyAdminsCanJoin and not msg.type.isSentByBotAdmin:
            self.globalMessage("{}, у тебя нет прав для входа в лобби.".format(sender))
            return
        if sender in self.bannedPlayers:
            self.globalMessage("{}, тебе ограничили возможность войти в лобби.".format(sender))
            return
        self.lobby.join(sender)

    def __leave(self, args: ARGS_DICT) -> None:
        if self.lobby is None:
            self.globalMessage("Лобби не было создано, но эта команда сработала? ЧТО-ТО НЕ ТАК!")
            return

        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        self.lobby.leave(msg.sender)

    def __kick(self, args: ARGS_DICT) -> None:
        if self.lobby is None:
            self.globalMessage("Лобби не было создано, но эта команда сработала? ЧТО-ТО НЕ ТАК!")
            return

        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        sender = msg.sender
        if not msg.type.isSentByBotAdmin:
            self.globalMessage("{}, у тебя нет прав для исключения игроков.".format(sender))
            return
        kiking = args["name"]
        if kiking not in self.lobby.players:
            self.globalMessage("Игрок {} не находится в лобби".format(kiking))
            return
        elif kiking == sender:
            self.whisperMessage("Невозможно исключить самого себя из лобби", sender)
            return

        self.lobby.leave(kiking)

        banned = ("doBan" in args) and (args["doBan"] == 'y')
        if banned:
            self.bannedPlayers.append(kiking)

    def __players(self, args: ARGS_DICT) -> None:
        if self.lobby is None:
            self.globalMessage("Лобби не было создано, но эта команда сработала? ЧТО-ТО НЕ ТАК!")
            return

        # TODO: ограничить использование
        self.globalMessage("Сейчас в лобби ({}/{}): {}"
                           .format(len(self.lobby.players),
                                   self.lobby.playerSettings.maxPlayersInLobby,
                                   self.lobby.players))

    def __close(self, args: ARGS_DICT) -> None:
        if self.lobby is None:
            self.globalMessage("Лобби не было создано, но эта команда сработала? ЧТО-ТО НЕ ТАК!")
            return

        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        sender = msg.sender
        if not msg.type.isSentByBotAdmin:
            self.globalMessage("{}, у тебя нет прав для закрытия лобби.".format(sender))
            return

        self.lobby.close()

        self.__onLobbyClosure()
