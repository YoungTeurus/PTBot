from typing import Callable, Optional

from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.SelfAwareChatObserver import SelfAwareChatObserver
from modules.base.Command import Command, CommandArg
from modules.commands.CommandParser import CommandParser
from properties import COMMAND_PREFIX
from utils.ConsoleProvider import ConsoleProvider

# (name, msg.sender, args, reason) => None
ACTION_ON_COMMAND_ERROR_HANDLER = Callable[[str, str, list[str], str], None]
# (msg) => action
NON_COMMAND_MSG_HANDLER = Callable[[ChatMessage], NotifyAction]


class CommandDrivenModule(SelfAwareChatObserver):
    """
    Модуль для работы с командами - сообщениями в чате, начинающимися со спецсимвола, при обработке которых необходимо
    выполнить какое-либо действие.
    """
    cp: ConsoleProvider
    # name => Command
    commands: dict[str, Command]
    # (name, msg.sender, args, reason) => None
    actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER
    actionOnNonCommandInput: Optional[NON_COMMAND_MSG_HANDLER]
    acceptNonCommandInputWithPrefix: bool

    def __init__(self, cp: ConsoleProvider, actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER = None,
                 actionOnNonCommandInput: NON_COMMAND_MSG_HANDLER = None,
                 acceptNonCommandInputWithPrefix: bool = False):
        self.cp = cp
        self.commands = {}
        self.actionOnCommandError = actionOnCommandError
        self.actionOnNonCommandInput = actionOnNonCommandInput
        self.acceptNonCommandInputWithPrefix = acceptNonCommandInputWithPrefix

    def addCommand(self, chatCommand: Command):
        self.commands[chatCommand.name] = chatCommand

    def addCommandCheckIfExists(self, chatCommand: Command):
        if chatCommand.name in self.commands:
            self.cp.print("Command '' was already in this module")
        self.addCommand(chatCommand)

    def doOnOtherMessage(self, msg: ChatMessage) -> NotifyAction:
        if not msg.body.startswith(COMMAND_PREFIX):
            if self.actionOnNonCommandInput is not None:
                return self.actionOnNonCommandInput(msg)
            return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
        bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
        command, args = CommandParser.getCommandAndArgs(bodyWithoutPrefix)

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

    def onError(self, command: str, msgSender: str, args: list[str], reason: str) -> None:
        self.cp.print("Ошибка в команде '{}', отправитель = '{}', арг-ы = '{}', причина = '{}'"
                      .format(command, msgSender, args, reason))
        if self.actionOnCommandError is not None:
            self.actionOnCommandError(command, msgSender, args, reason)

    def __getArgsValidateErrors(self, msg: ChatMessage,
                                commandArgs: list[CommandArg],
                                actualArgs: list[str]) -> list[str]:
        errors = []

        for comArg, actualArg in zip(commandArgs, actualArgs):
            if comArg.predicate is not None:
                if not comArg.predicate.validate(actualArg, msg, actualArgs):
                    errors.append(comArg.predicate.getValidationErrorText(actualArg, msg, actualArgs))

        return errors
