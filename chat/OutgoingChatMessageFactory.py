from chat.ChatMessage import ChatMessage
from properties import DEFAULT_LOG_BOT_NICKNAME
from utils.BotProperites import BotProperties


class OutgoingChatMessageFactory:
    botProperties: BotProperties

    def __init__(self, botProperties: BotProperties):
        self.botProperties = botProperties

    def globalMsg(self, body: str) -> ChatMessage:
        builder = self.__createBaseMessage(body)
        return builder.build()

    def whisperMsg(self, body: str, to: str) -> ChatMessage:
        builder = self.__createBaseMessage(body)

        builder.receiver = to
        builder.type.isWhisper = True

        return builder.build()

    def __createBaseMessage(self, body: str) -> ChatMessage.Builder:
        builder = ChatMessage.Builder()

        builder.type.isSentByBot = True
        if self.botProperties.botName is not None:
            builder.sender = self.botProperties.botName
        else:
            builder.sender = DEFAULT_LOG_BOT_NICKNAME
        builder.body = body

        return builder
