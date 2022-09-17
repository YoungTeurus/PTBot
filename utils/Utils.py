from typing import Callable, TypeVar

from selenium.webdriver.remote.webelement import WebElement

T = TypeVar('T')

CALLBACK_FUNCTION = Callable[[], None]
T_SUPPLIER = Callable[[], T]
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
