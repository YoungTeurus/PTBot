from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement

from driver.ElementManipulator import ElementManipulator
from utils.WebElementFunctions import SEND_KEYS, IS_NOT_INTRACTABLE

chatInputXPath = '//*[@id="chat-input"]'
openChatBoxButtonXPath = '//*[@id="chat-box"]/ui-button'


class ChatSender:
    manipulator: ElementManipulator

    def __init__(self, manipulator: ElementManipulator):
        self.manipulator = manipulator

    def sendMessage(self, message: str) -> None:
        self.manipulator.findOneAndCheck(chatInputXPath, IS_NOT_INTRACTABLE, self.__openChat)
        self.manipulator.findOneAndApply(chatInputXPath, SEND_KEYS(message + Keys.RETURN),
                                         onFail=lambda: print("Failed to send message '{}'".format(message)))

    def __openChat(self, _: WebElement) -> None:
        self.manipulator.findOneAndClick(openChatBoxButtonXPath)
