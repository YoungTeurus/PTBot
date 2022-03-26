from time import sleep

from selenium.webdriver import Chrome

from bot.BotWorkersContainer import BotWorkersContainer
from bot.workers.ChatSenderWorker import ChatSenderWorker
from chat.ChatReader import ChatReader
from chat.ChatParser import ChatParser
from chat.ChatSender import ChatSender
from chat.ChatSenderQuerySender import ChatSenderQuerySender
from driver.DriverInitializer import DriverInitializer
from driver.ElementManipulator import ElementManipulator
from driver.LocalStorage import LocalStorage
from workflow import logInPT, enterGame

if __name__ == "__main__":
    driver: Chrome = DriverInitializer.startDriver()
    localStorage: LocalStorage = LocalStorage(driver)
    logInPT(driver)
    manipulator: ElementManipulator = ElementManipulator(driver)
    enterGame(manipulator)

    ch = ChatReader(manipulator, localStorage)
    cp = ChatParser()
    cs = ChatSender(manipulator)

    csqs = ChatSenderQuerySender(cs)
    bwc = BotWorkersContainer()

    bwc.addWorker(ChatSenderWorker(csqs))
