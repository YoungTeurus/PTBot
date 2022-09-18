from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.Command import CommandArg
from modules.base.CommandDrivenModule import Command
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenModule
from utils.ConsoleProvider import ConsoleProvider
from utils.Utils import CALLBACK_FUNCTION


class SwitchableParrot(OutputtingCommandDrivenModule):
    enabled: bool

    argsToCallback: dict[str, CALLBACK_FUNCTION]

    def __init__(self, cp: ConsoleProvider, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory):
        super().__init__(cp, csqs, ocmf, actionOnNonCommandInput=self.doParrot)
        self.enabled = False

        self.argsToCallback = {
            "вкл": self.turnOn,
            "выкл": self.turnOff
        }

        optionalArgs = [CommandArg("newState")]

        self.addCommand(Command("попуг", self.doSwitch, optionalArgs=optionalArgs))

    def doSwitch(self, msg: ChatMessage, args: list[str]) -> None:
        if msg.type.isSentByBotAdmin:
            if len(args) == 0:
                self.switch()
            else:
                newState = args[0]
                if newState in self.argsToCallback:
                    self.argsToCallback[newState]()
        else:
            self.csqs.addGlobalMessage('Ты недостоин!', self.ocmf)

    def switch(self) -> None:
        newEnabled = not self.enabled
        if newEnabled:
            self.turnOn()
        else:
            self.turnOff()

    def turnOn(self) -> None:
        self.enabled = True
        self.csqs.addGlobalMessage('Попугай активирован!', self.ocmf)

    def turnOff(self) -> None:
        self.enabled = False
        self.csqs.cleanMsgQueue()
        self.csqs.addGlobalMessage('Попугай деактивирован!', self.ocmf)

    def doParrot(self, msg: ChatMessage) -> NotifyAction:
        if self.enabled:
            self.csqs.addGlobalMessage('{} сказал(а) {}'.format(msg.sender, msg.body), self.ocmf)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
