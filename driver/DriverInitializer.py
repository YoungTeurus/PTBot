from selenium.webdriver import Firefox, Chrome

from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox
from selenium.webdriver.firefox.webdriver import WebDriver

from properties import PATH_TO_CHROME_DRIVER, PATH_TO_FIREFOX_DRIVER


class DriverInitializer:
    @staticmethod
    def startChromeDriver() -> Chrome:
        service = ServiceChrome(executable_path=PATH_TO_CHROME_DRIVER)
        return Chrome(service=service)

    @staticmethod
    def startFirefoxDriver() -> WebDriver:
        service = ServiceFirefox(executable_path=PATH_TO_FIREFOX_DRIVER)
        return Firefox(service=service)
