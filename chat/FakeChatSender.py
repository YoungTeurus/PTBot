from chat.ChatMessage import ChatMessage
from chat.ChatProvider import ChatProvider
from utils.ConsoleProvider import ConsoleProvider


class FakeChatSender:
    chatProvider: ChatProvider
    cp: ConsoleProvider

    def __init__(self, chatProvider: ChatProvider, cp: ConsoleProvider):
        self.chatProvider = chatProvider
        self.cp = cp

    def sendMessage(self, message: ChatMessage) -> None:
        """
        Логирует то, что бот хотел отправить в игровой чат и
        отправляет это в chatProvider, как если бы бот
        действительно отправил это сообщение (бот услышит сам себя).
        """
        self.cp.print("Bot tried to send message to chat: {}".format(message))
        self.chatProvider.cleanAndAddMultipleMessages([message])
