from selenium.webdriver.remote.webelement import WebElement

from driver.ElementManipulator import ElementManipulator
from driver.LocalStorage import LocalStorage
from utils.BotProperites import BotProperties, BotState

lastMsgIdLSKey = 'last-message-id'
chatStr = '//*[@id="chat-log"]/div/div[2]/div[2]/div/div'


class ChatReader:
    bp: BotProperties
    manipulator: ElementManipulator
    localStorage: LocalStorage
    lastHeardMsgId: int

    def __init__(self, bp: BotProperties, manipulator: ElementManipulator, localStorage: LocalStorage):
        self.bp = bp
        self.manipulator = manipulator
        self.localStorage = localStorage
        self.lastHeardMsgId = self.__getLastMsgId()

    def __getLastMsgId(self) -> int:
        return int(self.localStorage.get(lastMsgIdLSKey))

    def __getAllChatDivs(self) -> list[WebElement]:
        return self.manipulator.findAllOrElse(chatStr, lambda: [])

    def getAllNewChatDivs(self) -> list[WebElement]:
        if self.bp.state < BotState.ENTERED_GAME:
            return []

        newLastHeardMsgId = self.__getLastMsgId()
        newMessageCount = newLastHeardMsgId - self.lastHeardMsgId
        if newMessageCount == 0:
            return []

        divs = self.__getAllChatDivs()
        newDivsCount = min(len(divs), newMessageCount)
        newDivs = divs[-newDivsCount:]

        self.lastHeardMsgId = newLastHeardMsgId

        return newDivs
