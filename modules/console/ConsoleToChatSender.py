from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.Command import Command, CommandArg, ARGS_DICT
from modules.base.CommandProvider import CommandProvider
from utils.ConsoleProvider import ConsoleProvider
from utils.Utils import addBotInputPrefix


class ConsoleToChatSender(CommandProvider):
    cp: ConsoleProvider
    csqs: ChatSenderQuerySender
    ocmf: OutgoingChatMessageFactory

    def __init__(self, cp: ConsoleProvider, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory):
        self.cp = cp
        self.csqs = csqs
        self.ocmf = ocmf

    def getConsoleCommands(self) -> list[Command]:
        optionalArgs = [
            CommandArg("body"),
        ]

        return [Command("send", self.sendMessageFromConsoleToChat, optionalArgs=optionalArgs)]

    def sendMessageFromConsoleToChat(self, args: ARGS_DICT) -> None:
        newMsg: ChatMessage
        if "body" not in args:
            newMsg = self.cp.runInConsoleLockWithResult(self.__inputMessage)
        elif len(args) == 1:
            newMsg = self.ocmf.globalMsg(args["body"])

        self.csqs.addMessage(newMsg)

    def __inputMessage(self) -> ChatMessage:
        body = input(addBotInputPrefix("Input message body: "))
        toWhisper = input(addBotInputPrefix("Send to bot as whisper? (y - yes) "))

        if toWhisper == "y":
            receiver = input(addBotInputPrefix("Input receiver: "))
            return self.ocmf.whisperMsg(body, receiver)
        else:
            return self.ocmf.globalMsg(body)
