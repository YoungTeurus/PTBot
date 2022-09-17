from typing import Callable

from selenium.webdriver.remote.webelement import WebElement

CALLBACK_FUNCTION = Callable[[], None]
ELEMENT_SUPPLIER = Callable[[], WebElement]
ELEMENTS_SUPPLIER = Callable[[], list[WebElement]]
ELEMENT_CALLBACK = Callable[[WebElement], None]
ELEMENTS_CALLBACK = Callable[[list[WebElement]], None]
ELEMENT_PREDICATE = Callable[[WebElement], bool]

STRING_PREDICATE = Callable[[str], bool]
STRING_CONSUMER = Callable[[str], None]


def runtimeErrorSupplier(msg: str) -> CALLBACK_FUNCTION:
    def wrapper():
        raise RuntimeError(msg)

    return wrapper
