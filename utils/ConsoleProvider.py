from threading import Lock

from utils.Utils import T_SUPPLIER, T


class ConsoleProvider:
    lock: Lock

    def __init__(self):
        self.lock = Lock()

    def print(self, output: object):
        with self.lock:
            print(output)

    def input(self, prompt: object) -> str:
        with self.lock:
            return input(prompt)

    def runInConsoleLockWithResult(self, func: T_SUPPLIER) -> T:
        with self.lock:
            return func()
