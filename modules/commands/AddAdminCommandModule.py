from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.Command import CHAT_MESSAGE_KEY, ARGS_DICT, CommandArg, Command
from modules.base.CommandProvider import CommandProvider
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenChatObserver
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import CONSOLE


class AddAdminCommandModule(OutputtingCommandDrivenChatObserver, CommandProvider):
    bp: BotProperties

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory,
                 bp: BotProperties):
        super().__init__(csqs, ocmf)
        self.bp = bp

    def _getInitialCommands(self) -> list[Command]:
        return [Command("op", self.chatAddOp, optionalArgs=[CommandArg("nick")])]

    def _getConsoleCommands(self) -> list[Command]:
        return [Command("op", self.consoleAddOp, [CommandArg("nick")])]

    def chatAddOp(self, args: ARGS_DICT) -> None:
        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        if not msg.type.isSentByBotAdmin:
            CONSOLE.print("User '{}' tried to add new admin but was not admin".format(msg.sender))
            return
        newAdminNick: str
        if "nick" not in args:
            newAdminNick = msg.sender
        else:
            newAdminNick = args["nick"]
        self.__addOp(newAdminNick)
        self.whisperMessage("Для '{}' установлен статус администратора".format(newAdminNick), msg.sender)

    def consoleAddOp(self, args: ARGS_DICT) -> None:
        newAdminNick = args["nick"]
        self.__addOp(newAdminNick)

    def __addOp(self, newAdminNick: str) -> None:
        CONSOLE.print("Adding '{}' as bot admin...".format(newAdminNick))
        self.whisperMessage("Получены права администратора", newAdminNick)
        self.bp.admins.append(newAdminNick)
