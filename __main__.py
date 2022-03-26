from time import sleep

from selenium.webdriver import Chrome

from bot.BotActionSubscriber import BotActionProcessor, ChatSenderWorker
from chat.ChatReader import ChatReader
from chat.ChatParser import ChatParser
from chat.ChatSender import ChatSender
from chat.ChatSenderController import ChatSenderController
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

    chatBox = '//*[@id="chat-log"]/div/div[2]/div[2]/div'
    chatLine = 'div'

    ch = ChatReader(manipulator, localStorage)
    cp = ChatParser()
    cs = ChatSender(manipulator)

    csc = ChatSenderController(cs)
    bap = BotActionProcessor()

    bap.addWorker(ChatSenderWorker(csc))

    sleep(5)
    for i in range(5):
        csc.addMessageToQuery("msg {}".format(i))
