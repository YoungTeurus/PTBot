from modules.base.Command import Command


class CommandProvider:
    """
    Класс, реализующий данный интерфейс предоставляет список команд для выполнения через консоль.
    """
    def getConsoleCommands(self) -> list[Command]:
        raise NotImplementedError
