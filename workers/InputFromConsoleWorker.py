from chat.ChatMessage import ChatMessage
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from utils.Utils import STRING_CONSUMER
from workers.interfaces.BaseBotWorker import BaseBotWorker
from workers.interfaces.WorkLockingBaseBotWorker import WorkLockingBaseBotWorker


class ConsoleInputConsumer(BaseBotWorker):
    """
    Воркер ожидает сообщения в консоли и пересылает их в метод, который был передан ему при инициализации.
    """
    inputConsumer: STRING_CONSUMER

    def __init__(self, inputConsumer: STRING_CONSUMER):
        super().__init__()
        self.inputConsumer = inputConsumer

    def _doWhileRunning(self) -> None:
        msg = input("Send this message: ")
        self.inputConsumer(msg)


class InputFromConsoleWorker(WorkLockingBaseBotWorker):
    csqs: ChatSenderQuerySender
    msgToSend: list[ChatMessage]
    test: ConsoleInputConsumer

    def __init__(self, csqs: ChatSenderQuerySender):
        super().__init__()

        self.csqs = csqs
        self.msgToSend = []

    def postInit(self) -> None:
        self.test = ConsoleInputConsumer(self.onNewInput)
        self.test.prepare(None)

    def onNewInput(self, msg: str) -> None:
        print("К нам пришёл инпут из консоли: {}".format(msg))

    def doWork(self) -> None:
        self.csqs.addMessages(self.msgToSend)
        self.msgToSend.clear()

    def hasWork(self) -> bool:
        return len(self.msgToSend) > 0

    def interrupt(self):
        super().interrupt()
        if self.test is not None:
            self.test.interrupt()
