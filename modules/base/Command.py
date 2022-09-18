from typing import Callable, Optional

from chat.ChatMessage import ChatMessage

# (args) => None
ACTION_CALLBACK = Callable[[ChatMessage, list[str]], None]


class CommandArgPredicate:
    """
    Предикат для команды чата - валидирует один аргумент чата, имея доступ ко всему сообщению и другим аргументам.
    """

    def validate(self, arg: str, msg: ChatMessage, args: list[str]) -> bool:
        """
        Валидирует аргумент команды.
        :param arg: Валидируемый аргумент
        :param msg: Сообщение с командой
        :param args: Все аргументы
        :return: Результат валидации, True - пройдена, False - не пройдена и можно запросить текст ошибки с
         помощью метода getValidationErrorText.
        """
        raise NotImplementedError

    def getValidationErrorText(self, arg: str, msg: ChatMessage, args: list[str]) -> str:
        raise NotImplementedError


class CommandArg:
    """
    Аргумент для команды чата.
    Хранит своё название и предикат, который используется для проверки аргумента на валидность.
    """
    name: str
    predicate: Optional[CommandArgPredicate]

    def __init__(self, name: str, predicate: CommandArgPredicate = None):
        self.name = name
        self.predicate = predicate


class Command:
    """
    Команда. Регистрация команды (через чат или в консоли) предполагает выполнение действия.
    Для команды могут передаваться как обязательные, так и необязательные аргументы.
    Необязательные аргументы всегда следуют после обязательных.
    Порядок аргументов задаётся порядком объектов в списке args и optionalArgs.
    """
    name: str
    action: ACTION_CALLBACK
    args: list[CommandArg]
    optionalArgs: list[CommandArg]

    def __init__(self, command: str, action: ACTION_CALLBACK,
                 args: list[CommandArg] = None, optionalArgs: list[CommandArg] = None):
        self.name = command
        self.action = action
        self.args = args if args is not None else []
        self.optionalArgs = optionalArgs if optionalArgs is not None else []
