from threading import Lock

from activities.BaseActivity import BaseActivity
from utils.ConsoleProvider import ConsoleProvider


class ActivityContainer:
    lock: Lock
    activities: list[BaseActivity]
    cp: ConsoleProvider

    def __init__(self, cp: ConsoleProvider):
        self.lock = Lock()
        self.activities = []
        self.cp = cp

    def add(self, activity: BaseActivity) -> None:
        def selfRemoveWrapper() -> None:
            self.__remove(activity)

        self.activities.append(activity)
        self.cp.print("Activity '{}' was added".format(activity))
        activity.prepare(self.lock, selfRemoveWrapper)

    def __remove(self, activity: BaseActivity) -> None:
        self.activities.remove(activity)

    def updateAll(self) -> None:
        for activity in self.activities:
            activity.doUpdate()

    def size(self) -> int:
        return len(self.activities)
