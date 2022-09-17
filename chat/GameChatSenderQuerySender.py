from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessagePreprocessor import OutgoingChatMessagePreprocessor
from chat.interfaces.ChatSender import ChatSender
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from utils.ConsoleProvider import ConsoleProvider


class GameChatSenderQuerySender(ChatSenderQuerySender):
    __chatSender: ChatSender
    cp: ConsoleProvider
    __sendQuery: list[str]

    def __init__(self, chatSender: ChatSender, cp: ConsoleProvider):
        self.__chatSender = chatSender
        self.cp = cp
        self.__sendQuery = []

    def addMessage(self, msg: ChatMessage) -> None:
        self.__sendQuery.extend(OutgoingChatMessagePreprocessor.prepareMessage(msg))

    def sendNextMessage(self) -> None:
        try:
            msgToSend = self.__sendQuery.pop(0)
            self.cp.print("Sending message '{}'".format(msgToSend))
            self.__chatSender.sendMessage(msgToSend)
        except IndexError:
            self.cp.print("Tried to send message while not having one in queue")
        except RuntimeError as err:
            self.cp.print("Error happened while sending message: {}".format(err))

    def hasMsgs(self) -> bool:
        return len(self.__sendQuery) > 0
