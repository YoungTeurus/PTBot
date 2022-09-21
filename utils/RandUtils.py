from random import choice

from utils.Utils import T


def randFromArr(arr: list[T]) -> T:
    return choice(arr)


def randPopFromArr(arr: list[T]) -> T:
    t = choice(arr)
    arr.remove(t)
    return t
