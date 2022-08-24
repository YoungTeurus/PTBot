import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from chat.ChatMessage import ChatMessage, ChatMessageType


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
        nameIndex: str = chatLineDiv.find_element(By.XPATH, "./*[@class='chat-line-name']/*[@class='chat-line-name-index']").text
        if nameIndex is not None and len(nameIndex) > 0:
            name += nameIndex
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
                builder.receiver = name
            else:
                builder.sender = name
        elif type.isAnnouncement or type.isSystem:
            builder.sender = name if len(name) > 0 else None
        else:
            builder.sender = name
        builder.type = type
        builder.body = body

        return builder.build()
