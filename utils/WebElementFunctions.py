import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement

from utils.Utils import ELEMENT_CALLBACK


def NO_ACTION() -> None:
    pass


def NO_ELEMENT_ACTION(element: WebElement) -> None:
    pass


def CLICK_ELEMENT(element: WebElement) -> None:
    element.click()


def SEND_KEYS(keys: str) -> ELEMENT_CALLBACK:
    def wrapper(element: WebElement):
        # for key in keys:
        #     element.send_keys(key)
        #     # time.sleep(0.01)
        element.send_keys(keys)
    return wrapper


def IS_INTERACTIVE(element: WebElement) -> bool:
    return element.is_displayed()


def IS_NOT_INTERACTIVE(element: WebElement) -> bool:
    return not element.is_displayed()
