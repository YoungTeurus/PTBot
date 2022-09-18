from typing import Callable

from modules.base.Command import Command

# (name, args) => None
ON_ERROR_HANDLER = Callable[[str, list[str]], None]


class CommandController:
    """
    Содержит и исполняет команды, которые можно запускать из командной строки
    """

    # (Command.name) => Command
    commands: dict[str, Command]

    def __init__(self):
        self.commands = {}

    def addCommands(self, commands: list[Command]) -> None:
        for com in commands:
            self.addCommand(com)

    def addCommand(self, command: Command) -> None:
        self.commands[command.name] = command

    def executeCommand(self, command: str, args: list[str], onError: ON_ERROR_HANDLER = None):
        if command in self.commands:
            self.commands[command].action(None, args)
        elif onError is not None:
            onError(command, args)
