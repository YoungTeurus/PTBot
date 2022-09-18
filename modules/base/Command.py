from typing import Callable, Union

from chat.ChatMessage import ChatMessage

# arg_name => arg_value
ARGS_DICT = dict[str, Union[ChatMessage, str]]
# (args_dict) => None
ACTION_CALLBACK = Callable[[ARGS_DICT], None]

# Зарезервированный ключ для ARGS_DICT, в котором располагается сообщение из чата.
CHAT_MESSAGE_KEY = "chatMsg"


class CommandArgValidator:
    """
    Предикат для команды - валидирует все её аргументы
    """

    def validate(self, args: ARGS_DICT) -> bool:
        """
        Валидирует аргументы команды.
        :param args: Все аргументы
        :return: Результат валидации, True - пройдена, False - не пройдена и можно запросить текст ошибки с
         помощью метода getValidationErrorText.
        """
        raise NotImplementedError

    def getValidationErrorText(self, args: ARGS_DICT) -> str:
        raise NotImplementedError


class CommandArg:
    """
    Аргумент для команды чата.
    Хранит своё название.
    """
    name: str

    def __init__(self, name: str):
        self.name = name


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
    validators: list[CommandArgValidator]

    def __init__(self, command: str, action: ACTION_CALLBACK,
                 args: list[CommandArg] = None, optionalArgs: list[CommandArg] = None,
                 validators: list[CommandArgValidator] = None):
        self.name = command
        self.action = action
        self.args = args if args is not None else []
        self.optionalArgs = optionalArgs if optionalArgs is not None else []
        self.validators = validators if validators is not None else []

    def checkArgsLength(self, args: list[str]) -> int:
        """
        :return: Отрицательное число - аргументов меньше, чем число требуемых.
         Положительное число - аргументов больше, чем сумма требуемых и опциональных аргументов.
         0 - длина аругментов подходящая.
        """
        if len(args) > len(self.args + self.optionalArgs):
            return 1
        elif len(args) < len(self.args):
            return -1
        return 0

    def createArgsDict(self, args: list[str]) -> ARGS_DICT:
        result = {}

        for actualArg, commandArg in zip(args, self.args + self.optionalArgs):
            result[commandArg.name] = actualArg

        return result
