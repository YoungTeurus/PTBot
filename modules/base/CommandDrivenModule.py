from typing import Callable, Optional

from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction
from properties import COMMAND_PREFIX
from utils.ArgsDevider import splitArgs
from utils.ConsoleProvider import ConsoleProvider

# (args) => None
ACTION_CALLBACK = Callable[[ChatMessage, list[str]], None]
# (command, msg.sender, args, reason) => None
ACTION_ON_COMMAND_ERROR_HANDLER = Callable[[str, str, list[str], str], None]


class ChatCommandArgPredicate:
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


class ChatCommandArg:
    """
    Аргумент для команды чата.
    Хранит своё название и предикат, который используется для проверки аргумента на валидность.
    """
    name: str
    predicate: Optional[ChatCommandArgPredicate]

    def __init__(self, name: str, predicate: ChatCommandArgPredicate = None):
        self.name = name
        self.predicate = predicate


class ChatCommand:
    """
    Команда для чата. Услышав команду в чате бот выполнит действие.
    Для команды могут передаваться как обязательные, так и необязательные аргументы.
    Необязательные аргументы всегда следуют после обязательных.
    Порядок аргументов задаётся порядком объектов в списке args и optionalArgs.
    """
    command: str
    action: ACTION_CALLBACK
    args: list[ChatCommandArg]
    optionalArgs: list[ChatCommandArg]

    def __init__(self, command: str, action: ACTION_CALLBACK,
                 args: list[ChatCommandArg] = None, optionalArgs: list[ChatCommandArg] = None):
        self.command = command
        self.action = action
        self.args = args if args is not None else []
        self.optionalArgs = optionalArgs if optionalArgs is not None else []


class CommandDrivenModule(ChatObserver):
    """
    Модуль для работы с командами - сообщениями в чате, начинающимися со спецсимвола, при обработке которых необходимо
    выполнить какое-либо действие.
    """
    cp: ConsoleProvider
    # command => ChatCommand
    commands: dict[str, ChatCommand]
    # (command, msg.sender, args, reason) => None
    actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER
    actionOnNonCommandInput: Optional[Callable[[ChatMessage], None]]
    acceptNonCommandInputWithPrefix: bool

    def __init__(self, cp: ConsoleProvider, actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER = None,
                 actionOnNonCommandInput: Callable[[ChatMessage], None] = None,
                 asseptNonCommandInputWithPrefix: bool = False):
        self.cp = cp
        self.commands = {}
        self.actionOnCommandError = actionOnCommandError
        self.actionOnNonCommandInput = actionOnNonCommandInput
        self.acceptNonCommandInputWithPrefix = asseptNonCommandInputWithPrefix

    def addCommand(self, chatCommand: ChatCommand):
        self.commands[chatCommand.command] = chatCommand

    def addCommandCheckIfExists(self, chatCommand: ChatCommand):
        if chatCommand.command in self.commands:
            self.cp.print("Command '' was already in this module")
        self.addCommand(chatCommand)

    def notify(self, msg: ChatMessage) -> NotifyAction:
        if not msg.body.startswith(COMMAND_PREFIX):
            if self.actionOnNonCommandInput is not None:
                self.actionOnNonCommandInput(msg)
            return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
        command, args = CommandDrivenModule.__getCommandAndArgs(msg.body)

        if command in self.commands:
            currentCommand = self.commands[command]
            if len(args) > len(currentCommand.args + currentCommand.optionalArgs):
                self.onError(command, msg.sender, args, "Length of args is more than args len for command")
            elif len(args) < len(currentCommand.args):
                self.onError(command, msg.sender, args, "Length of args is lesser than args len for command")
            else:
                validateErrors: list[str] = \
                    self.__getArgsValidateErrors(msg, currentCommand.args + currentCommand.optionalArgs, args)
                if len(validateErrors) == 0:
                    currentCommand.action(msg, args)
                else:
                    self.onError(command, msg.sender, args, "There was at least one problem with args validation: {}"
                                 .format(validateErrors))
        elif self.acceptNonCommandInputWithPrefix and self.actionOnNonCommandInput is not None:
            self.actionOnNonCommandInput(msg)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER

    @staticmethod
    def __getCommandAndArgs(msgBody: str) -> tuple[str, list[str]]:
        """
        Разделяет текст сообщения на саму команду и список аргументов.
        :param msgBody: Текст сообщения
        :return: Tuple, первый элемент - команда, второй элемент - список аргументов
        """
        msgWithoutPrefix = msgBody[len(COMMAND_PREFIX):]
        commandAndArgs = splitArgs(msgWithoutPrefix)
        command = commandAndArgs[0]
        args = commandAndArgs[1:]
        return command, args

    def onError(self, command: str, msgSender: str, args: list[str], reason: str) -> None:
        self.cp.print("Ошибка в команде '{}', отправитель = '{}', арг-ы = '{}', причина = '{}'"
                      .format(command, msgSender, args, reason))
        if self.actionOnCommandError is not None:
            self.actionOnCommandError(command, msgSender, args, reason)

    def __getArgsValidateErrors(self, msg: ChatMessage,
                                commandArgs: list[ChatCommandArg],
                                actualArgs: list[str]) -> list[str]:
        errors = []

        for comArg, actualArg in zip(commandArgs, actualArgs):
            if comArg.predicate is not None:
                if not comArg.predicate.validate(actualArg, msg, actualArgs):
                    errors.append(comArg.predicate.getValidationErrorText(actualArg, msg, actualArgs))

        return errors
