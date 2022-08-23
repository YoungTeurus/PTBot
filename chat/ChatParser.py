import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from chat.ChatMessage import ChatMessage, ChatMessageType, SYSTEM, BOT_NAME, EVERYONE


class ChatParser:
    @staticmethod
    def parseDiv(chatLineDiv: WebElement) -> ChatMessage:
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
        builder.type = type
        builder.lead = lead
        builder.timestamp = datetime.datetime.strptime(timestamp, "%H:%M")
        builder.label = label
        if type.isWhisper:
            msgText: str = chatLineDiv.text
            msgTextWithoutBody: str = msgText.removesuffix(body)
            hasPrefixTo: bool = msgTextWithoutBody[:msgTextWithoutBody.index('[')].find("To") >= 0

            if hasPrefixTo:
                builder.sender = BOT_NAME
                builder.receiver = name
            else:
                builder.sender = name
                builder.receiver = BOT_NAME
        elif type.isAnnouncement or type.isSystem:
            builder.receiver = BOT_NAME
            builder.sender = name if len(name) > 0 else None
        else:
            builder.sender = name
        builder.body = body

        return builder.build()
