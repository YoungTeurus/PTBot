from chat.ChatMessagePreprocessor import ChatMessagePreprocessor
from chat.ChatSender import ChatSender


class ChatSenderQuerySender:
    __chatSender: ChatSender
    __sendQuery: list[str]

    def __init__(self, chatSender: ChatSender):
        self.__chatSender = chatSender
        self.__sendQuery = []

    def addMessageToQuery(self, msg: str) -> None:
        self.__sendQuery.extend(ChatMessagePreprocessor.prepareMessageForGlobal(msg))

    def sendNextMessage(self) -> None:
        msgToSend = self.__sendQuery[0]
        try:
            print("Sending message '{}'".format(msgToSend))
            self.__chatSender.sendMessage(msgToSend)
            self.__sendQuery.remove(msgToSend)
        except RuntimeError as err:
            print(err)

    def hasMsgs(self) -> bool:
        return len(self.__sendQuery) > 0
