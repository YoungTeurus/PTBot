from chat.ChatSender import ChatSender


class ChatSenderController:
    chatSender: ChatSender
    sendQuery: list[str]

    def __init__(self, chatSender: ChatSender):
        self.chatSender = chatSender
        self.sendQuery = []

    def addMessageToQuery(self, msg: str) -> None:
        self.sendQuery.append(msg)

    def sendNextMessage(self) -> None:
        self.chatSender.sendMessage(self.sendQuery.pop(0))
