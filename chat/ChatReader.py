from selenium.webdriver.remote.webelement import WebElement

from driver.ElementManipulator import ElementManipulator
from driver.LocalStorage import LocalStorage

lastMsgIdLSKey = 'last-message-id'
chatStr = '//*[@id="chat-log"]/div/div[2]/div[2]/div/div'


class ChatReader:
    manipulator: ElementManipulator
    localStorage: LocalStorage
    lastHeardMsgId: int

    def __init__(self, manipulator: ElementManipulator, localStorage: LocalStorage):
        self.manipulator = manipulator
        self.localStorage = localStorage
        self.lastHeardMsgId = self.getLastMsgId()

    def getLastMsgId(self) -> int:
        return int(self.localStorage.get(lastMsgIdLSKey))

    def getAllChatDivs(self) -> list[WebElement]:
        return self.manipulator.findAllOrElse(chatStr, lambda: [])

    def getAllNewChatDivs(self) -> list[WebElement]:
        newLastHeardMsgId = self.getLastMsgId()
        newMessageCount = newLastHeardMsgId - self.lastHeardMsgId
        if newMessageCount == 0:
            return []

        divs = self.getAllChatDivs()
        newDivsCount = min(len(divs), newMessageCount)
        newDivs = divs[-newDivsCount:]

        self.lastHeardMsgId = newLastHeardMsgId

        return newDivs
