from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.Command import CommandArg, ARGS_DICT, CHAT_MESSAGE_KEY
from modules.base.CommandDrivenModule import Command
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenModule
from utils.ConsoleProvider import CONSOLE
from utils.Utils import CALLBACK_FUNCTION


class SwitchableParrot(OutputtingCommandDrivenModule):
    enabled: bool
    onlyAnonimous: bool

    argsToCallback: dict[str, CALLBACK_FUNCTION]

    def __init__(self, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory):
        super().__init__(csqs, ocmf, actionOnNonCommandInput=self.doParrot)
        self.enabled = False
        self.onlyAnonimous = False

        self.argsToCallback = {
            "вкл": self.turnOn,
            "выкл": self.turnOff,
            "аноним": self.turnAnonim,
        }

    def _getInitialCommands(self) -> list[Command]:
        return [Command("попуг", self.doSwitch, optionalArgs=[CommandArg("newState")])]

    def doSwitch(self, args: ARGS_DICT) -> None:
        msg: ChatMessage = args[CHAT_MESSAGE_KEY]
        if msg.type.isSentByBotAdmin:
            if "newState" not in args:
                self.switch()
            else:
                newState: str = args["newState"]
                if newState in self.argsToCallback:
                    self.argsToCallback[newState]()
        else:
            self.globalMessage('Ты недостоин взаимодействовать с моим тумблером!')

    def switch(self) -> None:
        newEnabled = not self.enabled
        if newEnabled:
            self.turnOn()
        else:
            self.turnOff()

    def turnOn(self) -> None:
        if self.enabled:
            self.globalMessage('Но я уже был включён!')
            return
        self.enabled = True
        self.onlyAnonimous = False
        self.globalMessage('Попугай активирован!')

    def turnOff(self) -> None:
        if not self.enabled:
            self.globalMessage('Но я уже был выключен!')
            return
        self.enabled = False
        self.onlyAnonimous = False
        self.csqs.cleanMsgQueue()
        self.globalMessage('Попугай деактивирован!')

    def turnAnonim(self) -> None:
        if not self.enabled:
            self.turnOn()
        self.onlyAnonimous = not self.onlyAnonimous
        if self.onlyAnonimous:
            self.globalMessage('Режим анонимки активирован!')
        else:
            self.globalMessage('Режим анонимки деактивирован!')

    def doParrot(self, msg: ChatMessage) -> NotifyAction:
        if self.enabled:
            if msg.type.isWhisper:
                self.globalMessage('Кто-то прошептал(а): "{}"'.format(msg.body))
            elif not self.onlyAnonimous:
                self.globalMessage('{} сказал(а): "{}"'.format(msg.sender, msg.body))
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
