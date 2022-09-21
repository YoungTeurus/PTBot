from chat.ChatObserver import NotifyAction
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.CommandDrivenChatObserver import ACTION_ON_COMMAND_ERROR_HANDLER, NON_COMMAND_MSG_HANDLER
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenChatObserver
from utils.Utils import STRING_CONSUMER, CALLBACK_FUNCTION


class MafiaWorker(OutputtingCommandDrivenChatObserver):
    waitingFor

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory,
                 actionOnCommandError: ACTION_ON_COMMAND_ERROR_HANDLER = None,
                 actionOnNonCommandInput: NON_COMMAND_MSG_HANDLER = None):
        super().__init__(csqs, ocmf, actionOnCommandError, actionOnNonCommandInput, True)

    def waitForAnswer(self, desiredSender: str, timeoutSecs: float,
                      onAnswerReceived: STRING_CONSUMER, onAnswerNotReceived: CALLBACK_FUNCTION):
        pass

    def onNonCommand(self) -> NotifyAction:
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
