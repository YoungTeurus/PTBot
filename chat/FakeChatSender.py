from chat.ChatMessage import ChatMessage
from chat.ChatProvider import ChatProvider

class FakeChatSender:
    chatProvider: ChatProvider

    def __init__(self, chatProvider: ChatProvider):
        self.chatProvider = chatProvider

    def sendMessage(self, message: ChatMessage) -> None:
        """
        Логирует то, что бот хотел отправить в игровой чат и
        отправляет это в chatProvider, как если бы бот
        действительно отправил это сообщение (бот услышит сам себя).
        """
        print("Bot tried to send message to chat: {}".format(message))
        self.chatProvider.cleanAndAddMultipleMessages([message])
