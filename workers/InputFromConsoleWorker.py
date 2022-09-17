from chat.ChatMessage import ChatMessage
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from utils.ConsoleProvider import ConsoleProvider
from utils.Utils import STRING_CONSUMER
from workers.interfaces.BaseBotWorker import BaseBotWorker
from workers.interfaces.WorkLockingBaseBotWorker import WorkLockingBaseBotWorker


class ConsoleInputConsumer(BaseBotWorker):
    """
    Воркер ожидает сообщения в консоли и пересылает их в метод, который был передан ему при инициализации.
    """
    inputConsumer: STRING_CONSUMER

    def __init__(self, cp: ConsoleProvider, inputConsumer: STRING_CONSUMER):
        super().__init__(cp)
        self.inputConsumer = inputConsumer

    def _doWhileRunning(self) -> None:
        input()
        msg = self.cp.input("Input message: ")
        self.inputConsumer(msg)


class InputFromConsoleWorker(WorkLockingBaseBotWorker):
    csqs: ChatSenderQuerySender
    msgToSend: list[ChatMessage]
    test: ConsoleInputConsumer

    def __init__(self, csqs: ChatSenderQuerySender, cp: ConsoleProvider):
        super().__init__(cp)

        self.csqs = csqs
        self.msgToSend = []
        self.cp = cp

    def postInit(self) -> None:
        self.test = ConsoleInputConsumer(self.cp, self.onNewInput)
        # noinspection PyTypeChecker
        self.test.prepare(None)

    def onNewInput(self, msg: str) -> None:
        self.cp.print("К нам пришёл инпут из консоли: {}".format(msg))

    def doWork(self) -> None:
        self.csqs.addMessages(self.msgToSend)
        self.msgToSend.clear()

    def hasWork(self) -> bool:
        return len(self.msgToSend) > 0

    def interrupt(self):
        super().interrupt()
        if self.test is not None:
            self.test.interrupt()
