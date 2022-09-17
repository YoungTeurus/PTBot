from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessagePreprocessor import OutgoingChatMessagePreprocessor
from chat.interfaces.ChatSender import ChatSender
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender


class GameChatSenderQuerySender(ChatSenderQuerySender):
    __chatSender: ChatSender
    __sendQuery: list[str]

    def __init__(self, chatSender: ChatSender):
        self.__chatSender = chatSender
        self.__sendQuery = []

    def addMessage(self, msg: ChatMessage) -> None:
        self.__sendQuery.extend(OutgoingChatMessagePreprocessor.prepareMessage(msg))

    def sendNextMessage(self) -> None:
        try:
            msgToSend = self.__sendQuery.pop(0)
            print("Sending message '{}'".format(msgToSend))
            self.__chatSender.sendMessage(msgToSend)
        except IndexError:
            print("Tried to send message while not having one in queue")
        except RuntimeError as err:
            print("Error happened while sending message: {}".format(err))

    def hasMsgs(self) -> bool:
        return len(self.__sendQuery) > 0
