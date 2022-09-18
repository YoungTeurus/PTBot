from chat.ChatMessage import ChatMessage
from chat.ChatObserver import NotifyAction
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.CommandDrivenModule import ChatCommand
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenModule
from utils.BotProperites import BotProperties
from utils.ConsoleProvider import ConsoleProvider


class SwitchableParrot(OutputtingCommandDrivenModule):
    bp: BotProperties

    enabled: bool

    def __init__(self, cp: ConsoleProvider, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory,
                 bp: BotProperties):
        super().__init__(cp, csqs, ocmf, actionOnNonCommandInput=self.doParrot)
        self.bp = bp

        self.enabled = False

        self.addCommand(ChatCommand("enable", self.doEnable))
        self.addCommand(ChatCommand("disable", self.doDisable))

    def doEnable(self, msg: ChatMessage, args: list[str]) -> None:
        if msg.sender in self.bp.admins:
            self.enabled = True
            self.csqs.addGlobalMessage('Попугай активирован!', self.ocmf)
        else:
            self.csqs.addGlobalMessage('Ты недостоин!', self.ocmf)

    def doDisable(self, msg: ChatMessage, args: list[str]) -> None:
        if msg.sender in self.bp.admins:
            self.enabled = False
            self.csqs.addGlobalMessage('Попугай деактивирован!', self.ocmf)
        else:
            self.csqs.addGlobalMessage('Ты не заткнёшь меня!', self.ocmf)

    def doParrot(self, msg: ChatMessage) -> NotifyAction:
        if self.enabled:
            self.csqs.addGlobalMessage('{} сказал(а) {}'.format(msg.sender, msg.body), self.ocmf)
        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
