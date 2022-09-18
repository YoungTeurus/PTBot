from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.CommandDrivenModule import Command, CommandArg
from modules.base.CommandProvider import CommandProvider
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenModule
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import ConsoleProvider


class AddAdminCommandModule(OutputtingCommandDrivenModule, CommandProvider):
    bp: BotProperties

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory, cp: ConsoleProvider,
                 bp: BotProperties):
        super().__init__(cp, csqs, ocmf)
        self.bp = bp

        optionalArgs = [CommandArg("nick")]

        command: Command = Command("op", self.addOp, optionalArgs=optionalArgs)

        self.addCommand(command)

    def getConsoleCommands(self) -> list[Command]:
        commands = []

        args = [CommandArg("nick")]

        commands.append(Command("op", self.noChatAddOp, args))

        return commands

    def noChatAddOp(self, msg: ChatMessage, args: list[str]) -> None:
        newAdminNick = args[0]
        self.cp.print("Adding '{}' as bot admin...".format(newAdminNick))
        self.bp.admins.append(newAdminNick)

    def addOp(self, msg: ChatMessage, args: list[str]) -> None:
        if not msg.type.isSentByBotAdmin:
            self.cp.print("User '{}' tried to add new admin but was not admin".format(msg.sender))
            return
        newAdminNick: str
        if len(args) == 0:
            newAdminNick = msg.sender
        else:
            newAdminNick = args[0]
        self.cp.print("Adding '{}' as bot admin...".format(newAdminNick))
        self.csqs.addWhisperMessage("Для '{}' установлен статус администратора".format(newAdminNick), msg.sender, self.ocmf)
        self.bp.admins.append(newAdminNick)
