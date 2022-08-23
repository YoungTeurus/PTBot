from time import time

from selenium.webdriver.remote.webelement import WebElement

from bot.workers.WorkLockingBaseBotWorker import WorkLockingBaseBotWorker
from chat.ChatHistory import ChatHistory
from chat.ChatMessage import ChatMessage
from chat.ChatParser import ChatParser
from chat.ChatReader import ChatReader
from properties import CHAT_READER_WORKER


class ChatReaderWorker(WorkLockingBaseBotWorker):
    chatReader: ChatReader
    chatParser: ChatParser
    chatHistory: ChatHistory
    lastCheckTime: float
    secsBetweenChecks: float = CHAT_READER_WORKER["secsBetweenChecks"]

    def __init__(self, chatReader: ChatReader, chatParser: ChatParser, chatHistory: ChatHistory):
        super(ChatReaderWorker, self).__init__()
        self.chatReader = chatReader
        self.chatParser = chatParser
        self.chatHistory = chatHistory

    def preInit(self) -> None:
        self.lastCheckTime = time()

    def hasWork(self) -> bool:
        return (time() - self.lastCheckTime) > self.secsBetweenChecks

    def doWork(self) -> None:
        newChatDivs: list[WebElement] = self.chatReader.getAllNewChatDivs()
        for chatDiv in newChatDivs:
            msg: ChatMessage = self.chatParser.parseDiv(chatDiv)
            self.chatHistory.appendHistory(msg)

        self.lastCheckTime = time()
