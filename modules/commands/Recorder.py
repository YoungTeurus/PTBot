from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.Command import ARGS_DICT, CHAT_MESSAGE_KEY
from modules.base.CommandDrivenModule import Command
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenModule
from utils.ConsoleProvider import ConsoleProvider


class Recorder(OutputtingCommandDrivenModule):
    """
    Позволяет записывать сообщения игроков и воспроизводить их.
    """
    # player_name => msgs
    history: dict[str, list[str]]

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory, cp: ConsoleProvider):
        super().__init__(cp, csqs, ocmf,
                         actionOnNonCommandInput=self.saveMessage,
                         acceptNonCommandInputWithPrefix=True)
        self.history = {}

        startCommand: Command = Command("start", self.startLogging)
        stopCommand: Command = Command("stop", self.stopLogging)

        self.addCommand(startCommand)
        self.addCommand(stopCommand)

    def startLogging(self, args: ARGS_DICT) -> None:
        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
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

    def stopLogging(self, args: ARGS_DICT) -> None:
        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
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
            for savedMsg in savedMessages:
                self.csqs.addGlobalMessage(savedMsg, self.ocmf)
        self.history.pop(msgSender)

    def saveMessage(self, msg: ChatMessage) -> NotifyAction:
        if msg.type.isSentByBot:
            return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
        msgSender = msg.sender
        if msgSender in self.history:
            msgBody = msg.body
            self.cp.print("Сохраняю сообщение от '{}' : '{}'".format(msgSender, msgBody))
            self.history[msgSender].append(msgBody)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
