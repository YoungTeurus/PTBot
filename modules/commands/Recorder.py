from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.Command import ARGS_DICT, CHAT_MESSAGE_KEY
from modules.base.CommandDrivenChatObserver import Command
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenChatObserver
from utils.ConsoleProvider import CONSOLE


class Recorder(OutputtingCommandDrivenChatObserver):
    """
    Позволяет записывать сообщения игроков и воспроизводить их.
    """
    # player_name => msgs
    history: dict[str, list[str]]

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory):
        super().__init__(csqs, ocmf,
                         acceptNonCommandInputWithPrefix=True)
        self.history = {}

    def _getInitialCommands(self) -> list[Command]:
        return [Command("start", self.startLogging), Command("stop", self.stopLogging)]

    def startLogging(self, args: ARGS_DICT) -> None:
        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        if msg.type.isSentByBot:
            return
        msgSender = msg.sender
        if msgSender in self.history:
            self.globalMessage("Уже слушаю сообщения от '{}', напишите '!stop' для остановки.".format(msgSender))
            return
        self.history[msgSender] = []
        self.globalMessage("Слушаю сообщения от '{}', напишите '!stop' для остановки...".format(msgSender))

    def stopLogging(self, args: ARGS_DICT) -> None:
        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        if msg.type.isSentByBot:
            return
        msgSender = msg.sender
        if msgSender not in self.history:
            self.globalMessage("Нет ни одного сохранённого сообщения от '{}'!".format(msgSender))
            return
        savedMessages = self.history[msgSender]
        msgCount = len(savedMessages)
        if msgCount == 0:
            self.globalMessage("Остановил запись сообщений от '{}', но вы не не оставили ни одного сообщения."
                               .format(msgSender))
        else:
            self.globalMessage("Повторяю все сообщения от '{}' в количестве {} штук(-и)..."
                               .format(msgSender, msgCount))
            for savedMsg in savedMessages:
                self.globalMessage(savedMsg)
        self.history.pop(msgSender)

    def onNonCommandInput(self, msg: ChatMessage, hasPrefix: bool) -> NotifyAction:
        if msg.type.isSentByBot:
            return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
        msgSender = msg.sender
        if msgSender in self.history:
            msgBody = msg.body
            CONSOLE.print("Сохраняю сообщение от '{}' : '{}'".format(msgSender, msgBody))
            self.history[msgSender].append(msgBody)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
