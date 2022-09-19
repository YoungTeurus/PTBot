from time import time

from selenium.webdriver.remote.webelement import WebElement

from chat.ChatMessage import ChatMessage
from chat.ChatParser import ChatParser
from chat.ChatProvider import ChatProvider
from chat.ChatReader import ChatReader
from chat.IncomingChatMessageProcessor import IncomingChatMessageProcessor
from properties import CHAT_READER_WORKER
from workers.base.WorkLockingBaseBotWorker import WorkLockingBaseBotWorker


class ChatReaderWorker(WorkLockingBaseBotWorker):
    chatReader: ChatReader
    chatParser: ChatParser
    chatProvider: ChatProvider
    chatMessageProcessor: IncomingChatMessageProcessor
    lastCheckTime: float
    secsBetweenChecks: float = CHAT_READER_WORKER["secsBetweenChecks"]

    def __init__(self, chatReader: ChatReader, chatParser: ChatParser, chatProvider: ChatProvider,
                 chatMessageProcessor: IncomingChatMessageProcessor):
        super().__init__()
        self.chatReader = chatReader
        self.chatParser = chatParser
        self.chatProvider = chatProvider
        self.chatMessageProcessor = chatMessageProcessor

    def preInit(self) -> None:
        self.lastCheckTime = time()

    def hasWork(self) -> bool:
        return (time() - self.lastCheckTime) > self.secsBetweenChecks

    def doWork(self) -> None:
        newChatDivs: list[WebElement] = self.chatReader.getAllNewChatDivs()
        newMsgs: list[ChatMessage] = []
        for chatDiv in newChatDivs:
            newMsg: ChatMessage = self.chatParser.parseDiv(chatDiv)
            self.chatMessageProcessor.process(newMsg)
            newMsgs.append(newMsg)
        self.chatProvider.cleanAndAddMultipleMessages(newMsgs)

        self.lastCheckTime = time()
