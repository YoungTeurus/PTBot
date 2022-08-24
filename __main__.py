import sys

from selenium.webdriver.firefox.webdriver import WebDriver

from bot.BotWorkersContainer import BotWorkersContainer
from bot.workers.ChatReaderWorker import ChatReaderWorker
from bot.workers.ChatSenderWorker import ChatSenderWorker
from chat.ChatMessageProcessor import ChatMessageProcessor
from chat.ChatProvider import ChatProvider
from chat.ChatReader import ChatReader
from chat.ChatParser import ChatParser
from chat.ChatSender import ChatSender
from chat.ChatSenderQuerySender import ChatSenderQuerySender
from driver.DriverInitializer import DriverInitializer
from driver.ElementManipulator import ElementManipulator
from driver.LocalStorage import LocalStorage
from modules.ChatToConsoleLogger import ChatToConsoleLogger
from modules.Parrot import Parrot
from modules.SelfIdentify import SelfIdentify
from modules.TestCommandModule import TestCommandModule
from modules.TestCommandWithHistoryModule import TestCommandWithHistoryModule
from utils.BotProperites import BotProperties
from workflow import logInPT, enterGame, getSkinName

if __name__ == "__main__":
    driver: WebDriver = DriverInitializer.startFirefoxDriver()
    localStorage: LocalStorage = LocalStorage(driver)

    bp = BotProperties()

    logInPT(driver)
    manipulator: ElementManipulator = ElementManipulator(driver)

    enterGame(manipulator)

    cr = ChatReader(manipulator, localStorage)
    cparse = ChatParser()
    cs = ChatSender(manipulator)
    cmp = ChatMessageProcessor(bp)

    bwc = BotWorkersContainer()

    csqs = ChatSenderQuerySender(cs)
    bwc.addWorker(ChatSenderWorker(csqs))

    cprovide = ChatProvider()
    cprovide.addObserver(ChatToConsoleLogger())

    bwc.addWorker(ChatReaderWorker(cr, cparse, cprovide, cmp))

    def updateBotNameAndLoadCustomModules(botName: str) -> None:
        bp.botName = botName
        loadCustomModules()

    def loadCustomModules() -> None:
        print("Loading custom modules (observers)...")
        cprovide.addObserver(Parrot(csqs))
        cprovide.addObserver(TestCommandWithHistoryModule(csqs))

    cprovide.addObserver(SelfIdentify(cprovide, csqs, updateBotNameAndLoadCustomModules))

