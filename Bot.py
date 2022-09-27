from typing import Callable

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
from modules.SelfIdentify import SelfIdentify
from modules.console.CommandController import CommandController
from utils.BotProperites import BotProperties, BotState
from utils.ConsoleProvider import CONSOLE
from workers.ActivityWorker import ActivityWorker
from workers.BotWorkersContainer import BotWorkersContainer
from workers.ChatReaderWorker import ChatReaderWorker
from workers.ChatSenderWorker import ChatSenderWorker
from workflow import logInPT, enterGame


class Bot:
    bp: BotProperties
    icmp: IncomingChatMessageProcessor
    bwc: BotWorkersContainer
    cprovide: ChatProvider
    ac: ActivityContainer
    ocmf: OutgoingChatMessageFactory
    csqs: ChatSenderQuerySender
    cc: CommandController

    def __init__(self, bp: BotProperties,
                 icmp: IncomingChatMessageProcessor,
                 bwc: BotWorkersContainer,
                 cprovide: ChatProvider,
                 ac: ActivityContainer,
                 ocmf: OutgoingChatMessageFactory,
                 csqs: ChatSenderQuerySender,
                 cc: CommandController):
        self.bp = bp
        self.icmp = icmp
        self.bwc = bwc
        self.cprovide = cprovide
        self.ac = ac
        self.ocmf = ocmf
        self.csqs = csqs
        self.cc = cc


def createBot(localMode: bool) -> Bot:
    bp = BotProperties()
    icmp = IncomingChatMessageProcessor(bp)
    bwc = BotWorkersContainer()
    cprovide = ChatProvider()
    ac = ActivityContainer()
    ocmf = OutgoingChatMessageFactory(bp)
    cc = CommandController()

    csqs: ChatSenderQuerySender

    if not localMode:
        driver: WebDriver = DriverInitializer.startFirefoxDriver()
        CONSOLE.print("Driver was initialized!")
        localStorage: LocalStorage = LocalStorage(driver)

        logInPT(driver)
        CONSOLE.print("Logged in PT!")
        manipulator: ElementManipulator = ElementManipulator(driver)

        enterGame(manipulator, bp)
        CONSOLE.print("Entered the game!")
        # waitForGameLoad(manipulator)

        cr = ChatReader(bp, manipulator, localStorage)
        cparse = ChatParser()
        cs = GameChatSender(manipulator)
        csqs = GameChatSenderQuerySender(cs)

        bwc.add(ChatReaderWorker(cr, cparse, cprovide, icmp))
        bwc.add(ChatSenderWorker(csqs))
    else:
        CONSOLE.print("Running in local mode!")
        cs = FakeChatSender(cprovide)
        csqs = FakeChatSenderQuerySender(cs)

    bot = Bot(bp, icmp, bwc, cprovide, ac, ocmf, csqs, cc)
    CONSOLE.print("Bot object was created!")
    __defaultConfig(bot)
    return bot


def __defaultConfig(bot: Bot) -> None:
    bot.cprovide.addObserver(ChatToConsoleLogger())
    bot.bwc.add(ActivityWorker(bot.ac))


def createAndInitBot(localMode: bool, afterInitCallback: Callable[[Bot], None]) -> Bot:
    bot = createBot(localMode)

    def updateBotNameAndState(botName: str) -> None:
        bot.bp.botName = botName
        bot.bp.state = BotState.INITIALIZED

    selfIdentify = SelfIdentify(bot.cprovide, bot.csqs, bot.ocmf, updateBotNameAndState)
    bot.cprovide.addObserver(selfIdentify)

    while bot.bp.state != BotState.INITIALIZED:
        pass

    afterInitCallback(bot)

    return bot
