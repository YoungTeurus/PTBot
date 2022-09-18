from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.CommandDrivenModule import CommandDrivenModule, ACTION_ON_COMMAND_ERROR_HANDLER, \
    NON_COMMAND_MSG_HANDLER
from utils.ConsoleProvider import ConsoleProvider


class OutputtingCommandDrivenModule(CommandDrivenModule):
    """
    Расширение модуля для работы с командами - добавлен стандартный обработчик ошибок и поля для работы с консолью.
    """
    csqs: ChatSenderQuerySender
    ocmf: OutgoingChatMessageFactory

    def __init__(self, cp: ConsoleProvider, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory,
                 actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER = None,
                 actionOnNonCommandInput: NON_COMMAND_MSG_HANDLER = None,
                 acceptNonCommandInputWithPrefix: bool = False):
        super().__init__(cp, actionOnCommandError if (actionOnCommandError is not None) else self.__defaultErrorHandler,
                         actionOnNonCommandInput,
                         acceptNonCommandInputWithPrefix)
        self.csqs = csqs
        self.ocmf = ocmf

    def __defaultErrorHandler(self, command: str, msgSender: str, args: list[str], reason: str) -> None:
        self.csqs.addGlobalMessage("Ошибка в команде '{}', отправитель = '{}', арг-ы = '{}', причина = '{}'"
                                   .format(command, msgSender, args, reason), self.ocmf)
