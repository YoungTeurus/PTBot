import random
import string
from typing import Callable

from chat.ChatMessage import ChatMessage
from chat.ChatObserver import ChatObserver, NotifyAction
from chat.ChatProvider import ChatProvider
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from properties import SELF_IDENTIFY_MESSAGE_LENGTH

# (botName) => None
END_SELF_IDENTIFY_CALLBACK = Callable[[str], None]


class SelfIdentify(ChatObserver):
    ch: ChatProvider
    csqs: ChatSenderQuerySender
    ocmf: OutgoingChatMessageFactory
    afterIdentifyCallback: END_SELF_IDENTIFY_CALLBACK

    identifyMessage: str | None

    def __init__(self, ch: ChatProvider, csqs: ChatSenderQuerySender, ocmf: OutgoingChatMessageFactory,
                 afterIdentifyCallback: END_SELF_IDENTIFY_CALLBACK):
        self.ch = ch
        self.csqs = csqs
        self.ocmf = ocmf
        self.afterIdentifyCallback = afterIdentifyCallback
        self.identifyMessage = None

    def startObserving(self) -> None:
        self.startIdentification()

    def startIdentification(self):
        self.identifyMessage = self.createIdentifyMessage()
        print("Sending '{}' to try to identify bot character...".format(self.identifyMessage))
        self.csqs.addGlobalMessage(self.identifyMessage, self.ocmf)

    def createIdentifyMessage(self) -> str:
        return SelfIdentify.randomword(SELF_IDENTIFY_MESSAGE_LENGTH)

    @staticmethod
    def randomword(length: int) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def notify(self, msg: ChatMessage) -> NotifyAction:
        if self.identifyMessage is not None:
            if msg.body == self.identifyMessage:
                self.ch.removeObserver(self)
                botName = msg.sender
                print("Bot name is '{}'".format(botName))
                self.afterIdentifyCallback(botName)

        return NotifyAction.CONTINUE_TO_NEXT_OBSERVER
