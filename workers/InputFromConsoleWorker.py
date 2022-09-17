from typing import Callable

from chat.ChatMessage import ChatMessage
from chat.ChatProvider import ChatProvider
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import ConsoleProvider
from workers.interfaces.BaseBotWorker import BaseBotWorker
from workers.interfaces.WorkLockingBaseBotWorker import WorkLockingBaseBotWorker

CHAT_MESSAGE_CONSUMER = Callable[[ChatMessage], None]


class ConsoleInputConsumer(BaseBotWorker):
    """
    Воркер ожидает сообщения в консоли и пересылает их в метод, который был передан ему при инициализации.
    """
    bp: BotProperties
    inputConsumer: CHAT_MESSAGE_CONSUMER

    def __init__(self, cp: ConsoleProvider, bp: BotProperties, chatMessageConsumer: CHAT_MESSAGE_CONSUMER):
        super().__init__(cp)
        self.bp = bp
        self.inputConsumer = chatMessageConsumer

    def _doWhileRunning(self) -> None:
        i = input()
        if len(i) > 0:
            msg = self.cp.runInConsoleLockWithResult(self.__inputMessage)
            self.inputConsumer(msg)

    def __inputMessage(self) -> ChatMessage:
        msg = input("Input message: ")
        sender = input("Send as: ")
        toWhisper = input("Send to bot as whisper? (y - yes) ")

        builder = ChatMessage.Builder()

        builder.body = msg
        builder.sender = sender
        if toWhisper == "y":
            builder.type.isWhisper = True
            builder.type.isSentToBot = True
            builder.receiver = self.bp.botName

        return builder.build()


class InputFromConsoleWorker(WorkLockingBaseBotWorker):
    cprovide: ChatProvider
    msgToReceive: list[ChatMessage]
    test: ConsoleInputConsumer
    bp: BotProperties

    def __init__(self, cprovide: ChatProvider, cp: ConsoleProvider, bp: BotProperties):
        super().__init__(cp)

        self.cprovide = cprovide
        self.msgToReceive = []
        self.cp = cp
        self.bp = bp

    def postInit(self) -> None:
        self.test = ConsoleInputConsumer(self.cp, self.bp, self.onNewInput)
        # noinspection PyTypeChecker
        self.test.prepare(None)

    def onNewInput(self, msg: ChatMessage) -> None:
        self.msgToReceive.append(msg)

    def doWork(self) -> None:
        self.cprovide.cleanAndAddMultipleMessages(self.msgToReceive)
        self.msgToReceive.clear()

    def hasWork(self) -> bool:
        return len(self.msgToReceive) > 0

    def interrupt(self):
        super().interrupt()
        if self.test is not None:
            self.test.interrupt()
