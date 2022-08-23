import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from chat.ChatMessage import ChatMessage, ChatMessageType, SYSTEM, BOT_NAME, EVERYONE
from utils.BotProperites import BotProperties


class ChatParser:
    botProperties: BotProperties

    def __init__(self, botProperties: BotProperties):
        self.botProperties = botProperties

    def parseDiv(self, chatLineDiv: WebElement) -> ChatMessage:
        classes: list[str] = chatLineDiv.get_attribute("class").split(" ")

        type = ChatMessageType()
        if "chat-line-whisper" in classes:
            type.isWhisper = True
        if "chat-line-system" in classes:
            type.isSystem = True
        if "chat-line-announcement" in classes:
            type.isAnnouncement = True
        if "chat-line-whisper-announcement" in classes:
            type.isWhisper = True
            type.isAnnouncement = True

        lead: str = chatLineDiv.find_element(By.XPATH, "./*[@class='chat-line-lead']").text
        timestamp: str = chatLineDiv.find_element(By.XPATH, "./*[@class='chat-line-timestamp']").text
        label: str = chatLineDiv.find_element(By.XPATH, "./*[@class='chat-line-label']").text
        name: str = chatLineDiv.find_element(By.XPATH, "./*[@class='chat-line-name']/*[@class='chat-line-name-content']").text
        body: str = chatLineDiv.find_element(By.XPATH, "./*[@class='chat-line-message']").text

        builder = ChatMessage.Builder()
        builder.lead = lead
        builder.timestamp = datetime.datetime.strptime(timestamp, "%H:%M")
        builder.label = label
        if type.isWhisper:
            msgText: str = chatLineDiv.text
            msgTextWithoutBody: str = msgText.removesuffix(body)
            hasPrefixTo: bool = msgTextWithoutBody[:msgTextWithoutBody.index('[')].find("To") >= 0

            if hasPrefixTo:
                builder.sender = self.botProperties.botName
                builder.receiver = name
            else:
                builder.sender = name
                builder.receiver = self.botProperties.botName
        elif type.isAnnouncement or type.isSystem:
            builder.receiver = self.botProperties.botName
            builder.sender = name if len(name) > 0 else None
        else:
            builder.sender = name
        if builder.sender == self.botProperties.botName:
            type.sentByBot = True
        builder.type = type
        builder.body = body

        return builder.build()
