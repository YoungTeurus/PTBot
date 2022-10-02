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

BOOL_PROVIDER = Callable[[], bool]


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


COUNT_DICT = dict[T, int]


def dictMostCommon(d: dict[T, int]) -> list[T]:
    mostCommon: list[T] = []
    mostCommonCount: int = -1
    for key in d:
        if (v := d[key]) < 0:
            raise ValueError("Count dict can't contain less than zero values")
        elif v > mostCommonCount:
            mostCommon = [key]
            mostCommonCount = v
        elif v == mostCommonCount:
            mostCommon.append(key)
    return mostCommon


if __name__ == "__main__":
    print(dictMostCommon({'a': 1, 'b': 2, 'c': 3}))
    print(dictMostCommon({'a': 1, 'b': 3, 'c': 3}))
    print(dictMostCommon({'a': 3, 'b': 2, 'c': 3}))
    print(dictMostCommon({}))


class MutableInt:
    value: int

    def __init__(self, value: int):
        self.value = value
