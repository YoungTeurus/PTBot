from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.CommandDrivenModule import CommandDrivenModule, ChatCommand


class TestCommandWithHistoryModule(CommandDrivenModule):
    csqs: ChatSenderQuerySender
    ocmf: OutgoingChatMessageFactory

    # player_name => msgs
    history: dict[str, list[str]]

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory):
        super().__init__(actionOnCommandError=self.sendErrorToChat,
                         actionOnNonCommandInput=self.saveMessage,
                         asseptNonCommandInputWithPrefix=True)
        self.csqs = csqs
        self.ocmf = ocmf
        self.history = {}

        startCommand: ChatCommand = ChatCommand("start", self.startLogging)
        stopCommand: ChatCommand = ChatCommand("stop", self.stopLogging)

        self.addCommand(startCommand)
        self.addCommand(stopCommand)

    def sendErrorToChat(self, command: str, msgSender: str, args: list[str], reason: str) -> None:
        self.csqs.addGlobalMessage("Error! command = {}, msgSender = {}, args = {}, reason = {}"
                                   .format(command, msgSender, args, reason), self.ocmf)

    def startLogging(self, msg: ChatMessage, args: list[str]) -> None:
        if msg.type.isSentByBot:
            return
        msgSender = msg.sender
        if msgSender in self.history:
            self.csqs.addGlobalMessage(
                "Уже слушаю сообщения от '{}', напишите '!stop' для остановки.".format(msgSender), self.ocmf)
            return
        self.history[msgSender] = []
        self.csqs.addGlobalMessage(
            "Слушаю сообщения от '{}', напишите '!stop' для остановки...".format(msgSender), self.ocmf)

    def stopLogging(self, msg: ChatMessage, args: list[str]) -> None:
        if msg.type.isSentByBot:
            return
        msgSender = msg.sender
        if msgSender not in self.history:
            self.csqs.addGlobalMessage("Нет ни одного сохранённого сообщения от '{}'!".format(msgSender),
                                       self.ocmf)
            return
        savedMessages = self.history[msgSender]
        msgCount = len(savedMessages)
        if msgCount == 0:
            self.csqs.addGlobalMessage(
                "Остановил запись сообщений от '{}', но вы не не оставили ни одного сообщения."
                .format(msgSender), self.ocmf)
        else:
            self.csqs.addGlobalMessage("Повторяю все сообщения от '{}' в количестве {} штук(-и)..."
                                       .format(msgSender, msgCount), self.ocmf)
            for msg in savedMessages:
                self.csqs.addGlobalMessage(msg, self.ocmf)
        self.history.pop(msgSender)

    def saveMessage(self, msg: ChatMessage) -> None:
        if msg.type.isSentByBot:
            return
        msgSender = msg.sender
        if msgSender in self.history:
            msgBody = msg.body
            print("Сохраняю сообщение от '{}' : '{}'".format(msgSender, msgBody))
            self.history[msgSender].append(msgBody)
