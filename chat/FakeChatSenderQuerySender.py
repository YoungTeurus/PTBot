from chat.ChatMessage import ChatMessage
from chat.FakeChatSender import FakeChatSender
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender


class FakeChatSenderQuerySender(ChatSenderQuerySender):
    __chatSender: FakeChatSender

    def __init__(self, fakeChatSender: FakeChatSender):
        self.__chatSender = fakeChatSender

    def addMessage(self, msg: ChatMessage) -> None:
        # Сразу отправляет сообщение без добавления в очередь
        self.__chatSender.sendMessage(msg)

    def sendNextMessage(self) -> None:
        pass

    def hasMsgs(self) -> bool:
        return False
