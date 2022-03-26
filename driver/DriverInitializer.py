from selenium.webdriver import Chrome

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from properties import PATH_TO_CHROME_DRIVER


class DriverInitializer:
    @staticmethod
    def startDriver() -> Chrome:
        service = Service(executable_path=PATH_TO_CHROME_DRIVER)
        options = Options()
        # options.add_argument("--headless")
        return Chrome(service=service, options=options)
