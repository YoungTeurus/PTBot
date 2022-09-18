from chat.ChatMessage import ChatMessage
from chat.IncomingChatMessageProcessor import IncomingChatMessageProcessor
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.Command import Command, CommandArg
from modules.base.CommandProvider import CommandProvider
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import ConsoleProvider
from utils.Utils import addBotInputPrefix


class ConsoleToChatSender(CommandProvider):
    cp: ConsoleProvider
    bp: BotProperties
    csqs: ChatSenderQuerySender
    icmp: IncomingChatMessageProcessor

    def __init__(self, cp: ConsoleProvider, bp: BotProperties, csqs: ChatSenderQuerySender, icmp: IncomingChatMessageProcessor):
        self.cp = cp
        self.bp = bp
        self.csqs = csqs
        self.icmp = icmp

    def getConsoleCommands(self) -> list[Command]:

        optionalArgs = [
            CommandArg("sender"),
            CommandArg("body"),
        ]

        return [Command("chat", self.sendMessageFromConsoleToChat, optionalArgs=optionalArgs)]

    def sendMessageFromConsoleToChat(self, msg: ChatMessage, args: list[str]) -> None:
        newMsg: ChatMessage
        if len(args) == 0:
            newMsg = self.cp.runInConsoleLockWithResult(self.__inputMessage)
        elif len(args) == 2:
            newMsg = self.__createMessage(args[0], args[1]).build()
        else:
            self.cp.print(addBotInputPrefix("Wrong number of args, expected 0 or 2 - sender and body"))
            return
        self.icmp.process(newMsg)
        self.csqs.addMessages([newMsg])

    def __inputMessage(self) -> ChatMessage:
        sender = input(addBotInputPrefix("Send as: "))
        body = input(addBotInputPrefix("Input message body: "))
        toWhisper = input(addBotInputPrefix("Send to bot as whisper? (y - yes) "))

        builder = self.__createMessage(sender, body)

        if toWhisper == "y":
            builder.type.isWhisper = True
            builder.type.isSentToBot = True
            builder.receiver = self.bp.botName

        return builder.build()

    @staticmethod
    def __createMessage(sender: str, body: str) -> ChatMessage.Builder:
        builder = ChatMessage.Builder()

        builder.sender = sender
        builder.body = body

        return builder
