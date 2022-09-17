from selenium.webdriver.firefox.webdriver import WebDriver

from activities.ActivityContainer import ActivityContainer
from chat.ChatParser import ChatParser
from chat.ChatProvider import ChatProvider
from chat.ChatReader import ChatReader
from chat.FakeChatSender import FakeChatSender
from chat.FakeChatSenderQuerySender import FakeChatSenderQuerySender
from chat.GameChatSender import GameChatSender
from chat.GameChatSenderQuerySender import GameChatSenderQuerySender
from chat.IncomingChatMessageProcessor import IncomingChatMessageProcessor
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from chat.interfaces.ChatSenderQuerySender import ChatSenderQuerySender
from driver.DriverInitializer import DriverInitializer
from driver.ElementManipulator import ElementManipulator
from driver.LocalStorage import LocalStorage
from modules.ChatToConsoleLogger import ChatToConsoleLogger
from modules.Parrot import Parrot
from modules.SelfIdentify import SelfIdentify
from modules.TestCommandWithHistoryModule import TestCommandWithHistoryModule
from properties import LOCAL_MODE
from utils.BotProperites import BotProperties, BotState
from workers.ActivityWorker import ActivityWorker
from workers.BotWorkersContainer import BotWorkersContainer
from workers.ChatReaderWorker import ChatReaderWorker
from workers.ChatSenderWorker import ChatSenderWorker
from workflow import logInPT, enterGame

if __name__ == "__main__":
    print("Starting bot...")

    bp = BotProperties()
    cmp = IncomingChatMessageProcessor(bp)

    bwc = BotWorkersContainer()

    cprovide = ChatProvider()
    cprovide.addObserver(ChatToConsoleLogger())

    ac = ActivityContainer()
    bwc.add(ActivityWorker(ac))

    ocmf = OutgoingChatMessageFactory(bp)

    csqs: ChatSenderQuerySender

    if not LOCAL_MODE:
        driver: WebDriver = DriverInitializer.startFirefoxDriver()
        print("Driver was initialized!")
        localStorage: LocalStorage = LocalStorage(driver)

        logInPT(driver)
        print("Logged in PT!")
        manipulator: ElementManipulator = ElementManipulator(driver)

        enterGame(manipulator)
        print("Entered the game!")
        # waitForGameLoad(manipulator)

        cr = ChatReader(manipulator, localStorage)
        cparse = ChatParser()
        cs = GameChatSender(manipulator)
        csqs = GameChatSenderQuerySender(cs)

        bwc.add(ChatReaderWorker(cr, cparse, cprovide, cmp))
        bwc.add(ChatSenderWorker(csqs))
    else:
        print("Running in local mode!")
        cs = FakeChatSender(cprovide)
        csqs = FakeChatSenderQuerySender(cs)

    def updateBotNameAndLoadCustomModules(botName: str) -> None:
        bp.botName = botName
        bp.state = BotState.INITIALIZED
        loadCustomModules()


    def loadCustomModules() -> None:
        print("Loading custom modules (observers)...")
        cprovide.addObserver(Parrot(csqs, ocmf))
        cprovide.addObserver(TestCommandWithHistoryModule(csqs, ocmf))
        print("Finished loading custom modules!")


    cprovide.addObserver(SelfIdentify(cprovide, csqs, ocmf, updateBotNameAndLoadCustomModules))
