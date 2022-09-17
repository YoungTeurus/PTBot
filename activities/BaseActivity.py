from threading import Lock

from utils.ConsoleProvider import ConsoleProvider
from utils.Utils import CALLBACK_FUNCTION


class BaseActivity:
    cp: ConsoleProvider
    lock: Lock
    running: bool
    selfRemove: CALLBACK_FUNCTION

    def __init__(self, cp: ConsoleProvider):
        self.running = False
        self.cp = cp

    def prepare(self, lock: Lock, selfRemove: CALLBACK_FUNCTION) -> None:
        self.cp.print("Activity '{}' is preparing...".format(self))

        self.lock = lock
        self.selfRemove = selfRemove
        self.setup()
        self.running = True

        self.cp.print("Activity '{}' is prepared".format(self))

    def setup(self) -> None:
        """
        Выполняется один раз - при запуске активити.
        """
        pass

    def doUpdate(self) -> None:
        if self.running:
            self.update()

    def update(self) -> None:
        """
        Выполняется при каждом обновлении контейнера.
        """
        pass
