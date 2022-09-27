from selenium.webdriver.firefox.webdriver import WebDriver

from driver.ElementManipulator import ElementManipulator
from properties import LOGIN_SETTINGS, PONY_TOWN_URL
from utils.BotProperites import BotProperties, BotState
from utils.Utils import runtimeErrorSupplier


def logInPT(driver: WebDriver) -> None:
    driver.get(PONY_TOWN_URL)
    driver.add_cookie({"name": "remember_me",
                       "value": LOGIN_SETTINGS["remember_me"],
                       'sameSite': 'Strict'})
    driver.add_cookie({"name": "connect.sid",
                       "value": LOGIN_SETTINGS["connect.sid"],
                       'sameSite': 'Strict'})
    driver.refresh()


def enterGame(manipulator: ElementManipulator, bp: BotProperties) -> None:
    manipulator.findOneAndClick(
        "/html/body/pony-town-app/div[2]/main/home/div/div[2]/div/div/div[8]/play-box/div[1]/div/button[1]",
        orElse=runtimeErrorSupplier("Login failed! Check cookies!")
    )
    bp.state = BotState.ENTERED_GAME
