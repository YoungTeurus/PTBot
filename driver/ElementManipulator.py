from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from properties import WAIT_SETTINGS
from utils.Utils import CALLBACK_FUNCTION, ELEMENT_CALLBACK, ELEMENTS_CALLBACK, ELEMENTS_SUPPLIER, ELEMENT_SUPPLIER, \
    ELEMENT_PREDICATE
from utils.WebElementFunctions import CLICK_ELEMENT, NO_ACTION, NO_ELEMENT_ACTION


class WaitSettings:
    timeout: float
    pollFrequency: float

    def __init__(self, timeout: float, pollFrequency: float):
        self.timeout = timeout
        self.pollFrequency = pollFrequency


DEFAULT_WAIT_SETTINGS = WaitSettings(
    WAIT_SETTINGS["timeout"],
    WAIT_SETTINGS["pollFrequency"]
)


class ElementManipulator:
    driver: WebDriver

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def findAll(self, path: str, waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> list[WebElement]:
        """
        Ожидает появления элемента в DOM структуре по XPath path в течение timeout, опрашивая DOM каждые checkPeriod.
        :raises TimeoutException - Период ожидания истёк и элемент не появился
        :return: Элемент, после того как он появился на странице.
        """
        return WebDriverWait(self.driver, waitSettings.timeout, poll_frequency=waitSettings.pollFrequency) \
            .until(lambda dr: dr.find_elements(by=By.XPATH, value=path))

    def findAllOrElse(self, path: str, orElse: ELEMENTS_SUPPLIER,
                      waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> list[WebElement]:
        try:
            return self.findAll(path, waitSettings)
        except TimeoutException:
            return orElse()

    def findOne(self, path: str, waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> WebElement:
        """
        Ожидает появления элемента в DOM структуре по XPath path в течение timeout, опрашивая DOM каждые checkPeriod.
        :raises TimeoutException - Период ожидания истёк и элемент не появился
        :return: Элемент, после того как он появился на странице.
        """
        return self.findAll(path, waitSettings)[0]

    def findOneOrElse(self, path: str, orElse: ELEMENT_SUPPLIER,
                      waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> WebElement:
        """
        Ожидает появления элемента в DOM структуре по XPath path в течение timeout, опрашивая DOM каждые checkPeriod.
        :raises TimeoutException - Период ожидания истёк и элемент не появился
        :return: Элемент, после того как он появился на странице.
        """
        try:
            return self.findAll(path, waitSettings)[0]
        except TimeoutException:
            return orElse()

    # def findAllAndApply(self, path: str, applyFunc: ELEMENTS_CALLBACK, onFail: CALLBACK_FUNCTION = None,
    #                  waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> None:
    #     """
    #     Пытается найти элемент по path и применить к нему некое действие.
    #     Если элемент не найден, выполняет функцию onFail.
    #     """
    #     try:
    #         element = self.findAll(path, waitSettings=waitSettings)
    #         applyFunc(element)
    #     except TimeoutException as err:
    #         if onFail is None:
    #             raise err
    #         onFail()

    # def findAllAndApplyForEvery(self, path: str, applyFunc: ELEMENT_CALLBACK, onFail: CALLBACK_FUNCTION = None,
    #                          waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> None:
    #     """
    #     Пытается найти элемент по path и применить к нему некое действие.
    #     Если элемент не найден, выполняет функцию onFail.
    #     """
    #     try:
    #         for element in self.findAll(path, waitSettings=waitSettings):
    #             applyFunc(element)
    #     except TimeoutException as err:
    #         if onFail is None:
    #             raise err
    #         onFail()

    def findOneAndApply(self, path: str, applyFunc: ELEMENT_CALLBACK, onFail: CALLBACK_FUNCTION = None,
                        waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> None:
        """
        Пытается найти элемент по path и применить к нему некое действие.
        Если элемент не найден, выполняет функцию onFail.
        """
        try:
            element = self.findOne(path, waitSettings=waitSettings)
            applyFunc(element)
        except TimeoutException as err:
            if onFail is None:
                raise err
            onFail()

    def findOneAndCheck(self, path: str, predicate: ELEMENT_PREDICATE, onTrue: ELEMENT_CALLBACK,
                        onFalse: ELEMENT_CALLBACK = NO_ELEMENT_ACTION, onFail: CALLBACK_FUNCTION = None,
                        waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> None:
        try:
            element = self.findOne(path, waitSettings=waitSettings)
            if predicate(element):
                onTrue(element)
            else:
                onFalse(element)
        except TimeoutException as err:
            if onFail is None:
                raise err
            onFail()

    def findOneAndClick(self, path: str, orElse: CALLBACK_FUNCTION = NO_ACTION,
                        waitSettings: WaitSettings = DEFAULT_WAIT_SETTINGS) -> None:
        self.findOneAndApply(path, CLICK_ELEMENT, orElse, waitSettings=waitSettings)

    def getDriver(self) -> WebDriver:
        return self.driver
