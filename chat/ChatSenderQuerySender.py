from chat.ChatMessagePreprocessor import ChatMessagePreprocessor
from chat.ChatSender import ChatSender


class ChatSenderQuerySender:
    chatSender: ChatSender
    sendQuery: list[str]

    def __init__(self, chatSender: ChatSender):
        self.chatSender = chatSender
        self.sendQuery = []

    def addMessageToQuery(self, msg: str) -> None:
        self.sendQuery.extend(ChatMessagePreprocessor.prepareMessageForGlobal(msg))

    def sendNextMessage(self) -> None:
        self.chatSender.sendMessage(self.sendQuery.pop(0))
