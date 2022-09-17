from threading import Lock


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
