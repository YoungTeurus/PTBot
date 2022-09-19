from modules.base.Command import Command


class CommandProvider:
    """
    Класс, реализующий данный интерфейс предоставляет список команд для выполнения через консоль.
    """
    def _getConsoleCommands(self) -> list[Command]:
        raise NotImplementedError
