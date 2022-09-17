from threading import Lock

from utils.Utils import CALLBACK_FUNCTION


class BaseActivity:
    lock: Lock
    running: bool
    selfRemove: CALLBACK_FUNCTION

    def __init__(self):
        self.running = False

    def prepare(self, lock: Lock, selfRemove: CALLBACK_FUNCTION) -> None:
        print("Activity '{}' is preparing...".format(self))

        self.lock = lock
        self.selfRemove = selfRemove
        self.setup()
        self.running = True

        print("Activity '{}' is prepared".format(self))

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
