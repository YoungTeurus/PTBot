from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.CommandDrivenModule import ChatCommand, ChatCommandArg
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenModule
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import ConsoleProvider


class AddAdminCommandModule(OutputtingCommandDrivenModule):
    bp: BotProperties

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory, cp: ConsoleProvider,
                 bp: BotProperties):
        super().__init__(cp, csqs, ocmf)
        self.bp = bp

        optionalArgs = [ChatCommandArg("nick")]

        command: ChatCommand = ChatCommand("op", self.addOp, optionalArgs=optionalArgs)

        self.addCommand(command)

    def addOp(self, msg: ChatMessage, args: list[str]) -> None:
        if msg.sender not in self.bp.admins:
            self.cp.print("User '{}' tried to add new admin but was not admin".format(msg.sender))
            return
        newAdminNick: str
        if len(args) == 0:
            newAdminNick = msg.sender
        else:
            newAdminNick = args[0]
        self.cp.print("Adding '{}' as bot admin...".format(newAdminNick))
        self.bp.admins.append(newAdminNick)
