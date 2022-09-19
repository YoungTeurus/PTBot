from typing import Optional

from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from games.lobby.Lobby import Lobby, PlayerCountLobbySettings
from modules.base.Command import Command, CommandArg, ARGS_DICT, CHAT_MESSAGE_KEY
from modules.base.CommandDrivenModule import ACTION_ON_COMMAND_ERROR_HANDLER, NON_COMMAND_MSG_HANDLER
from modules.base.CommandProvider import CommandProvider
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenModule
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import CONSOLE


class LobbyCreator(OutputtingCommandDrivenModule, CommandProvider):
    bp: BotProperties

    lobby: Optional[Lobby]
    bannedPlayers: list[str]

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory, bp: BotProperties,
                 actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER = None,
                 actionOnNonCommandInput: NON_COMMAND_MSG_HANDLER = None,
                 acceptNonCommandInputWithPrefix: bool = False):
        super().__init__(csqs, ocmf, actionOnCommandError, actionOnNonCommandInput, acceptNonCommandInputWithPrefix)
        self.bp = bp

    def _getConsoleCommands(self) -> list[Command]:
        pass

    def _getInitialCommands(self) -> list[Command]:
        return [
            Command("лобби", self.__lobby),
        ]

    def __setCommandOnLobbyClose(self) -> None:
        commandsToAdd = [
            Command("лобби", self.__lobby),
        ]
        self.addCommands(commandsToAdd)
        commandsToRemove = ["настройка", "начать", "войти", "выйти", "выгнать", "игроки", "закрыть"]
        self.removeCommands(commandsToRemove)

    def __lobby(self, args: ARGS_DICT) -> None:
        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        if not msg.type.isSentByBotAdmin:
            self.globalMessage("{}, у тебя нет прав на создание лобби".format(msg.sender))

    def __onLobbyCreation(self) -> None:
        # TODO установка параметров лобби:
        settings = PlayerCountLobbySettings()
        self.lobby = Lobby(settings,
                           lambda players: CONSOLE.print("Lobby started with players {}".format(players)))
        self.__setCommandOnLobbyOpen()

    def __setCommandOnLobbyOpen(self) -> None:
        commandsToAdd = [
            Command("настройка", self.__settings, [CommandArg("name")], [CommandArg("value")]),
            Command("начать", self.__start, optionalArgs=[CommandArg("onlyAdmins")]),
            Command("войти", self.__join),
            Command("выйти", self.__leave),
            Command("выгнать", self.__kick, [CommandArg("name")], [CommandArg("doBan")]),
            Command("игроки", self.__players),
            Command("закрыть", self.__close),
        ]
        self.addCommands(commandsToAdd)
        commandsToRemove = ["лобби"]
        self.removeCommands(commandsToRemove)

    def __settings(self, args: ARGS_DICT) -> None:
        pass

    def __start(self, args: ARGS_DICT) -> None:
        pass

    def __create(self, args: ARGS_DICT) -> None:
        pass

    def __join(self, args: ARGS_DICT) -> None:
        pass

    def __leave(self, args: ARGS_DICT) -> None:
        pass

    def __kick(self, args: ARGS_DICT) -> None:
        pass

    def __players(self, args: ARGS_DICT) -> None:
        pass

    def __close(self, args: ARGS_DICT) -> None:
        pass
