from typing import Callable

from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction
from properties import COMMAND_PREFIX
from utils.Utils import STRING_PREDICATE

# (args) => None
ACTION_CALLBACK = Callable[[list[str]], None]
# (command, msg.sender, args, reason) => None
ACTION_ON_COMMAND_ERROR_HANDLER = Callable[[str, str, list[str], str], None]


class ChatCommandArg:
    name: str
    predicate: STRING_PREDICATE | None

    def __init__(self, name: str, predicate: STRING_PREDICATE | None = None):
        self.name = name
        self.predicate = predicate


class ChatCommand:
    command: str
    action: ACTION_CALLBACK
    args: list[ChatCommandArg]
    optionalArgs: list[ChatCommandArg]

    def __init__(self, command: str, action: ACTION_CALLBACK,
                 args: list[ChatCommandArg] | None = None, optionalArgs: list[ChatCommandArg] | None = None):
        self.command = command
        self.action = action
        self.args = args if args is not None else []
        self.optionalArgs = optionalArgs if optionalArgs is not None else []


class CommandDrivenModule(ChatObserver):
    # command => ChatCommand
    commands: dict[str, ChatCommand]
    # (command, msg.sender, args, reason) => None
    actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER

    def __init__(self, actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER = None):
        self.commands = {}
        self.actionOnCommandError = actionOnCommandError

    def addCommand(self, chatCommand: ChatCommand):
        self.commands[chatCommand.command] = chatCommand

    def addCommandCheckIfExists(self, chatCommand: ChatCommand):
        if chatCommand.command in self.commands:
            print("Command '' was already in this module")
        self.addCommand(chatCommand)

    def notify(self, msg: ChatMessage) -> NotifyAction:
        if not msg.body.startswith(COMMAND_PREFIX):
            return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
        command, args = CommandDrivenModule.getCommandAndArgs(msg.body)

        if command in self.commands:
            currentCommand = self.commands[command]
            if len(args) > len(currentCommand.args + currentCommand.optionalArgs):
                self.onError(command, msg.sender, args, "Length of args is more than args len for command")
            elif len(args) < len(currentCommand.args):
                self.onError(command, msg.sender, args, "Length of args is lesser than args len for command")
            currentCommand.action(args)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER

    @staticmethod
    def getCommandAndArgs(msgBody: str) -> tuple[str, list[str]]:
        # TODO: разделять по пробелам, позволяя вводить аргументы в кавычках
        commandAndArgs = msgBody[1:].split(" ")
        command = commandAndArgs[0]
        args = commandAndArgs[1:]
        return command, args

    def onError(self, command: str, msgSender: str, args: list[str], reason: str) -> None:
        print("Error! command = {}, msgSender = {}, args = {}, reason = {}".format(command, msgSender, args, reason))
        if self.actionOnCommandError is not None:
            self.actionOnCommandError(command, msgSender, args, reason)
