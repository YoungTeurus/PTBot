from typing import Callable, TypeVar

from selenium.webdriver.remote.webelement import WebElement

from properties import BOT_INPUT_PREFIX

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

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


def addBotInputPrefix(output: str) -> str:
    return BOT_INPUT_PREFIX + output


def dictUpdate(d: dict[K, V], key: K, updateFunc: Callable[[K, V], V]) -> None:
    if key in d:
        d[key] = updateFunc(key, d[key])
    else:
        d[key] = updateFunc(key, None)


def groupBy(objs: list[T], keyGetter: Callable[[T], K]) -> dict[K, list[T]]:
    grouped = {}
    for obj in objs:
        key: K = keyGetter(obj)
        dictUpdate(grouped, key, lambda k, v: v.append(obj) if v is not None else [obj])
    return grouped


class MutableInt:
    value: int

    def __init__(self, value: int):
        self.value = value
