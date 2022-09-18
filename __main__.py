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
from modules.ConsoleToChatSender import ConsoleToChatSender
from modules.SelfIdentify import SelfIdentify
from modules.commands.AddAdminCommandModule import AddAdminCommandModule
from modules.commands.Recorder import Recorder
from modules.commands.SwitchableParrot import SwitchableParrot
from modules.console.CommandController import CommandController
from properties import LOCAL_MODE
from utils.BotProperites import BotProperties, BotState
from utils.ConsoleProvider import ConsoleProvider
from workers.ActivityWorker import ActivityWorker
from workers.BotWorkersContainer import BotWorkersContainer
from workers.ChatReaderWorker import ChatReaderWorker
from workers.ChatSenderWorker import ChatSenderWorker
from workers.InputFromConsoleWorker import InputFromConsoleWorker
from workflow import logInPT, enterGame

if __name__ == "__main__":
    cp = ConsoleProvider()

    cp.print("Starting bot...")

    bp = BotProperties()
    icmp = IncomingChatMessageProcessor(bp)

    bwc = BotWorkersContainer(cp)

    cprovide = ChatProvider()
    cprovide.addObserver(ChatToConsoleLogger(cp))

    ac = ActivityContainer(cp)
    bwc.add(ActivityWorker(ac, cp))

    ocmf = OutgoingChatMessageFactory(bp)

    csqs: ChatSenderQuerySender

    cc = CommandController()

    if not LOCAL_MODE:
        driver: WebDriver = DriverInitializer.startFirefoxDriver()
        cp.print("Driver was initialized!")
        localStorage: LocalStorage = LocalStorage(driver)

        logInPT(driver)
        cp.print("Logged in PT!")
        manipulator: ElementManipulator = ElementManipulator(driver)

        enterGame(manipulator)
        cp.print("Entered the game!")
        # waitForGameLoad(manipulator)

        cr = ChatReader(manipulator, localStorage)
        cparse = ChatParser()
        cs = GameChatSender(manipulator)
        csqs = GameChatSenderQuerySender(cs, cp)

        bwc.add(ChatReaderWorker(cr, cparse, cprovide, icmp, cp))
        bwc.add(ChatSenderWorker(csqs, cp))
    else:
        cp.print("Running in local mode!")
        cs = FakeChatSender(cprovide)
        csqs = FakeChatSenderQuerySender(cs)


    def updateBotNameAndState(botName: str) -> None:
        bp.botName = botName
        bp.state = BotState.INITIALIZED


    def loadCustomModules() -> None:
        cp.print("Loading custom modules (observers)...")
        ifcw = InputFromConsoleWorker(cp, cc)
        bwc.add(ifcw)

        cc.addCommands(ConsoleToChatSender(cp, bp, csqs, icmp).getConsoleCommands())

        cprovide.addObserver(SwitchableParrot(cp, csqs, ocmf))
        cprovide.addObserver(Recorder(csqs, ocmf, cp))
        aacm = AddAdminCommandModule(csqs, ocmf, cp, bp)
        cc.addCommands(aacm.getConsoleCommands())
        cprovide.addObserver(aacm)
        cp.print("Finished loading custom modules!")


    selfIdentify = SelfIdentify(cprovide, csqs, ocmf, cp, updateBotNameAndState)
    cprovide.addObserver(selfIdentify)

    while bp.state != BotState.INITIALIZED:
        pass

    loadCustomModules()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        bwc.stopAll()
