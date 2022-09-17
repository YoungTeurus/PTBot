from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement

from chat.interfaces.ChatSender import ChatSender
from driver.ElementManipulator import ElementManipulator
from utils.Utils import runtimeErrorSupplier
from utils.WebElementFunctions import SEND_KEYS, IS_NOT_INTERACTIVE, IS_INTERACTIVE

chatInputXPath = '//textarea[contains(@class,"chat-textarea")]'
openChatBoxButtonXPath = '//*[@id="chat-box"]/ui-button'


class GameChatSender(ChatSender):
    manipulator: ElementManipulator

    def __init__(self, manipulator: ElementManipulator):
        self.manipulator = manipulator

    def sendMessage(self, message: str) -> None:
        self.manipulator.findOneAndCheck(chatInputXPath, IS_NOT_INTERACTIVE, self.__openChat)
        self.manipulator.findOneAndCheck(chatInputXPath, IS_INTERACTIVE, SEND_KEYS(message + Keys.RETURN),
                                         onFail=runtimeErrorSupplier("Failed to send message '{}'".format(message)))

    def __openChat(self, _: WebElement) -> None:
        self.manipulator.findOneAndClick(openChatBoxButtonXPath)
