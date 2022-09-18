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
    onlyAnonimous: bool

    argsToCallback: dict[str, CALLBACK_FUNCTION]

    def __init__(self, cp: ConsoleProvider, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory):
        super().__init__(cp, csqs, ocmf, actionOnNonCommandInput=self.doParrot)
        self.enabled = False
        self.onlyAnonimous = False

        self.argsToCallback = {
            "вкл": self.turnOn,
            "выкл": self.turnOff,
            "аноним": self.turnAnonim,
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
            self.csqs.addGlobalMessage('Ты недостоин взаимодействовать с моим тумблером!', self.ocmf)

    def switch(self) -> None:
        newEnabled = not self.enabled
        if newEnabled:
            self.turnOn()
        else:
            self.turnOff()

    def turnOn(self) -> None:
        if self.enabled:
            self.csqs.addGlobalMessage('Но я уже был включён!', self.ocmf)
            return
        self.enabled = True
        self.onlyAnonimous = False
        self.csqs.addGlobalMessage('Попугай активирован!', self.ocmf)

    def turnOff(self) -> None:
        if not self.enabled:
            self.csqs.addGlobalMessage('Но я уже был выключен!', self.ocmf)
            return
        self.enabled = False
        self.onlyAnonimous = False
        self.csqs.cleanMsgQueue()
        self.csqs.addGlobalMessage('Попугай деактивирован!', self.ocmf)

    def turnAnonim(self) -> None:
        if not self.enabled:
            self.turnOn()
        self.onlyAnonimous = not self.onlyAnonimous
        if self.onlyAnonimous:
            self.csqs.addGlobalMessage('Режим анонимки активирован!', self.ocmf)
        else:
            self.csqs.addGlobalMessage('Режим анонимки деактивирован!', self.ocmf)

    def doParrot(self, msg: ChatMessage) -> NotifyAction:
        if self.enabled:
            if msg.type.isWhisper:
                self.csqs.addGlobalMessage('Кто-то прошептал(а): "{}"'.format(msg.body), self.ocmf)
            elif not self.onlyAnonimous:
                self.csqs.addGlobalMessage('{} сказал(а): "{}"'.format(msg.sender, msg.body), self.ocmf)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
