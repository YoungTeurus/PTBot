from chat.ChatMessage import ChatMessage
from chat.ChatProvider import ChatProvider
from chat.IncomingChatMessageProcessor import IncomingChatMessageProcessor
from modules.base.Command import Command, CommandArg, ARGS_DICT
from modules.base.CommandProvider import CommandProvider
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import CONSOLE
from utils.Utils import addBotInputPrefix


class ConsoleToBotSender(CommandProvider):
    bp: BotProperties
    icmp: IncomingChatMessageProcessor
    cprovide: ChatProvider

    def __init__(self, bp: BotProperties, icmp: IncomingChatMessageProcessor,
                 cprovide: ChatProvider):
        self.bp = bp
        self.icmp = icmp
        self.cprovide = cprovide

    def getConsoleCommands(self) -> list[Command]:

        optionalArgs = [
            CommandArg("sender"),
            CommandArg("body"),
        ]

        return [Command("fakemsg", self.sendMessageFromConsoleToBot, optionalArgs=optionalArgs)]

    def sendMessageFromConsoleToBot(self, args: ARGS_DICT) -> None:
        newMsg: ChatMessage
        if "sender" in args and "body" in args:
            newMsg = self.__createMessage(args["sender"], args["body"]).build()
        else:
            newMsg = CONSOLE.runInConsoleLockWithResult(self.__inputMessage)
        self.icmp.process(newMsg)
        self.cprovide.cleanAndAddMultipleMessages([newMsg])

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
