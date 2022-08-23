from selenium.webdriver.firefox.webdriver import WebDriver

from bot.BotWorkersContainer import BotWorkersContainer
from bot.workers.ChatReaderWorker import ChatReaderWorker
from bot.workers.ChatSenderWorker import ChatSenderWorker
from chat.ChatHistory import ChatHistory
from chat.ChatReader import ChatReader
from chat.ChatParser import ChatParser
from chat.ChatSender import ChatSender
from chat.ChatSenderQuerySender import ChatSenderQuerySender
from driver.DriverInitializer import DriverInitializer
from driver.ElementManipulator import ElementManipulator
from driver.LocalStorage import LocalStorage
from modules.ConsoleHistoryWriter import ConsoleHistoryWriter
from modules.Parrot import Parrot
from modules.TestCommandModule import TestCommandModule
from modules.TestCommandWithHistoryModule import TestCommandWithHistoryModule
from workflow import logInPT, enterGame

if __name__ == "__main__":
    driver: WebDriver = DriverInitializer.startFirefoxDriver()
    localStorage: LocalStorage = LocalStorage(driver)
    logInPT(driver)
    manipulator: ElementManipulator = ElementManipulator(driver)
    enterGame(manipulator)

    cr = ChatReader(manipulator, localStorage)
    cp = ChatParser()
    cs = ChatSender(manipulator)

    bwc = BotWorkersContainer()

    csqs = ChatSenderQuerySender(cs)
    bwc.addWorker(ChatSenderWorker(csqs))

    ch = ChatHistory()
    ch.addObserver(ConsoleHistoryWriter())
    # ch.addObserver(Parrot(csqs))

    bwc.addWorker(ChatReaderWorker(cr, cp, ch))

    ch.addObserver(TestCommandWithHistoryModule(csqs))

