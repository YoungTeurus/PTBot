from chat.ChatMessage import ChatMessage
from chat.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.CommandDrivenModule import CommandDrivenModule, ACTION_CALLBACK, ChatCommand, ChatCommandArg


class TestCommandWithHistoryModule(CommandDrivenModule):
    csqs: ChatSenderQuerySender

    # player_name => msgs
    history: dict[str, list[str]]

    def __init__(self, csqs: ChatSenderQuerySender):
        super().__init__(actionOnCommandError=self.sayInChat,
                         actionOnNonCommandInput=self.saveMessage,
                         asseptNonCommandInputWithPrefix=True)
        self.csqs = csqs
        self.history = {}

        startCommand: ChatCommand = ChatCommand("start", self.startLogging)
        stopCommand: ChatCommand = ChatCommand("stop", self.stopLogging)

        self.addCommand(startCommand)
        self.addCommand(stopCommand)

    def sayInChat(self, command: str, msgSender: str, args: list[str], reason: str) -> None:
        self.csqs.addMessageToQuery("Error! command = {}, msgSender = {}, args = {}, reason = {}"
                                    .format(command, msgSender, args, reason))

    def startLogging(self, msg: ChatMessage, args: list[str]) -> None:
        msgSender = msg.sender
        if msgSender == "- Ma-Zee-ic -":
            return
        if msgSender in self.history:
            self.csqs.addMessageToQuery("Уже слушаю сообщения от '{}', напишите '!stop' для остановки.".format(msgSender))
            return
        self.history[msgSender] = []
        self.csqs.addMessageToQuery("Слушаю сообщения от '{}', напишите '!stop' для остановки...".format(msgSender))

    def stopLogging(self, msg: ChatMessage, args: list[str]) -> None:
        msgSender = msg.sender
        if msgSender == "- Ma-Zee-ic -":
            return
        if msgSender not in self.history:
            self.csqs.addMessageToQuery("Нет ни одного сохранённого сообщения от '{}'!".format(msgSender))
            return
        savedMessages = self.history[msgSender]
        msgCount = len(savedMessages)
        if msgCount == 0:
            self.csqs.addMessageToQuery("Остановил запись сообщений от '{}', но вы не не оставили ни одного сообщения."
                                        .format(msgSender))
        else:
            self.csqs.addMessageToQuery("Повторяю все сообщения от '{}' в количестве {} штук(-и)..."
                                        .format(msgSender, msgCount))
            for msg in savedMessages:
                self.csqs.addMessageToQuery(msg)
        self.history.pop(msgSender)

    def saveMessage(self, msg: ChatMessage) -> None:
        msgSender = msg.sender
        if msgSender == "- Ma-Zee-ic -":
            return
        if msgSender in self.history:
            msgBody = msg.body
            print("Сохраняю сообщение от '{}' : '{}'".format(msgSender, msgBody))
            self.history[msgSender].append(msgBody)
