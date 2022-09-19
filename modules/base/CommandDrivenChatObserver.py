from typing import Callable, Optional

from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.SelfAwareChatObserver import SelfAwareChatObserver
from modules.base.Command import Command, ARGS_DICT, CHAT_MESSAGE_KEY
from properties import COMMAND_PREFIX
from utils.CommandParser import CommandParser
from utils.ConsoleProvider import CONSOLE

# (name, msg.sender, args, reason) => None
ACTION_ON_COMMAND_ERROR_HANDLER = Callable[[str, str, list[str], str], None]
# (msg) => action
NON_COMMAND_MSG_HANDLER = Callable[[ChatMessage], NotifyAction]


class CommandDrivenChatObserver(SelfAwareChatObserver):
    """
    Модуль для работы с командами - сообщениями в чате, начинающимися со спецсимвола, при обработке которых необходимо
    выполнить какое-либо действие.
    """
    # name => Command
    commands: dict[str, Command]
    # (name, msg.sender, args, reason) => None
    actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER
    actionOnNonCommandInput: Optional[NON_COMMAND_MSG_HANDLER]
    acceptNonCommandInputWithPrefix: bool

    def __init__(self, actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER = None,
                 actionOnNonCommandInput: NON_COMMAND_MSG_HANDLER = None,
                 acceptNonCommandInputWithPrefix: bool = False):
        self.commands = {}
        self.actionOnCommandError = actionOnCommandError
        self.actionOnNonCommandInput = actionOnNonCommandInput
        self.acceptNonCommandInputWithPrefix = acceptNonCommandInputWithPrefix

        for command in self._getInitialCommands():
            self.addCommand(command)

    def _getInitialCommands(self) -> list[Command]:
        raise NotImplementedError

    def addCommands(self, chatCommands: list[Command]):
        for command in chatCommands:
            self.addCommand(command)

    def addCommand(self, chatCommand: Command):
        self.commands[chatCommand.name] = chatCommand

    def addCommandCheckIfExists(self, chatCommand: Command):
        if chatCommand.name in self.commands:
            CONSOLE.print("Command '' was already in this module")
        self.addCommand(chatCommand)

    def removeCommands(self, commandNames: list[str]):
        for commandName in commandNames:
            self.removeCommand(commandName)

    def removeCommand(self, commandName: str):
        if commandName in self.commands:
            self.commands.pop(commandName)

    def doOnOtherMessage(self, msg: ChatMessage) -> NotifyAction:
        if not msg.body.startswith(COMMAND_PREFIX):
            if self.actionOnNonCommandInput is not None:
                return self.actionOnNonCommandInput(msg)
            return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
        bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
        command, args = CommandParser.getCommandAndArgs(bodyWithoutPrefix)

        if command in self.commands:
            currentCommand = self.commands[command]
            argLenCheck = currentCommand.checkArgsLength(args)
            if argLenCheck > 0:
                self.onError(command, msg.sender, args, "Length of args is more than args len for command")
                return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
            elif argLenCheck < 0:
                self.onError(command, msg.sender, args, "Length of args is lesser than args len for command")
                return NotifyAction.CONTINUE_TO_NEXT_OBSERVER

            argsDict: ARGS_DICT = currentCommand.createArgsDict(args)
            argsDict[CHAT_MESSAGE_KEY] = msg

            validateErrors: list[str] = self.__getArgsValidateErrors(currentCommand, argsDict)
            if len(validateErrors) == 0:
                currentCommand.action(argsDict)
            else:
                self.onError(command, msg.sender, args, "There was at least one problem with args validation: {}"
                             .format(validateErrors))

        elif self.acceptNonCommandInputWithPrefix and self.actionOnNonCommandInput is not None:
            self.actionOnNonCommandInput(msg)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER

    @staticmethod
    def __checkArgsLength(command: Command, args: list[str]) -> int:
        if len(args) > len(command.args + command.optionalArgs):
            return 1
        elif len(args) < len(command.args):
            return -1
        return 0

    def onError(self, command: str, msgSender: str, args: list[str], reason: str) -> None:
        CONSOLE.print("Ошибка в команде '{}', отправитель = '{}', арг-ы = '{}', причина = '{}'"
                      .format(command, msgSender, args, reason))
        if self.actionOnCommandError is not None:
            self.actionOnCommandError(command, msgSender, args, reason)

    @staticmethod
    def __getArgsValidateErrors(command: Command, args: ARGS_DICT) -> list[str]:
        errors = []

        for validator in command.validators:
            if not validator.validate(args):
                errors.append(validator.getValidationErrorText(args))

        return errors
