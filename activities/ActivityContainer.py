from threading import Lock

from activities.BaseActivity import BaseActivity


class ActivityContainer:
    lock: Lock
    activities: list[BaseActivity]

    def __init__(self):
        self.lock = Lock()
        self.activities = []

    def add(self, activity: BaseActivity) -> None:
        def selfRemoveWrapper() -> None:
            self.__remove(activity)

        self.activities.append(activity)
        print("Activity '{}' was added".format(activity))
        activity.prepare(self.lock, selfRemoveWrapper)

    def __remove(self, activity: BaseActivity) -> None:
        self.activities.remove(activity)

    def updateAll(self) -> None:
        for activity in self.activities:
            activity.doUpdate()
