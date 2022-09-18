from modules.commands.CommandParser import CommandParser
from modules.console.CommandController import CommandController
from utils.ConsoleProvider import ConsoleProvider
from utils.TimedInput import input_with_timeout, TimeoutExpired
from utils.Utils import STRING_CONSUMER, addBotInputPrefix
from workers.base.BaseBotWorker import BaseBotWorker
from workers.base.WorkLockingBaseBotWorker import WorkLockingBaseBotWorker


class ConsoleInputConsumer(BaseBotWorker):
    """
    Воркер ожидает сообщения в консоли и пересылает их в метод, который был передан ему при инициализации.
    """
    inputConsumer: STRING_CONSUMER

    def __init__(self, cp: ConsoleProvider, inputConsumer: STRING_CONSUMER):
        super().__init__(cp)
        self.inputConsumer = inputConsumer

    def _doWhileRunning(self) -> None:
        try:
            i = input_with_timeout(timeout=1)
            if len(i) > 0:
                command = self.cp.runInConsoleLockWithResult(self.__inputCommand)
                if len(command.strip()) > 0:
                    self.inputConsumer(command)
                else:
                    self.cp.print(addBotInputPrefix("No command found"))
        except TimeoutExpired:
            pass

    @staticmethod
    def __inputCommand() -> str:
        return input(addBotInputPrefix("Input command: "))


class InputFromConsoleWorker(WorkLockingBaseBotWorker):
    cic: ConsoleInputConsumer
    cc: CommandController

    def __init__(self, cp: ConsoleProvider, cc: CommandController):
        super().__init__(cp)
        self.cp = cp
        self.cc = cc

    def postInit(self) -> None:
        self.cic = ConsoleInputConsumer(self.cp, self.onNewInput)
        # noinspection PyTypeChecker
        self.cic.prepare(None)

    def onNewInput(self, input: str) -> None:
        command, args = CommandParser.getCommandAndArgs(input)
        self.cc.executeCommand(command, args)

    def interrupt(self):
        super().interrupt()
        if self.cic is not None:
            self.cic.interrupt()
