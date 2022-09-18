from chat.ChatMessage import ChatMessage
from utils.BotProperites import BotProperties


class IncomingChatMessageProcessor:
    botProperties: BotProperties

    def __init__(self, botProperties: BotProperties):
        self.botProperties = botProperties

    def process(self, msg: ChatMessage) -> None:
        self.__checkMessageOnBotName(msg)
        self.__checkMessageOnAdminSender(msg)

    def __checkMessageOnBotName(self, msg: ChatMessage) -> None:
        botName = self.botProperties.botName
        if botName is not None:
            if msg.type.isSentByBot:
                msg.sender = botName
            elif msg.sender == botName:
                msg.type.isSentByBot = True
            elif msg.type.isSentToBot:
                msg.receiver = botName

    def __checkMessageOnAdminSender(self, msg: ChatMessage) -> None:
        if msg.sender in self.botProperties.admins:
            msg.type.isSentByBotAdmin = True
