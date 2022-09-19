from time import time

from activities.ActivityContainer import ActivityContainer
from properties import ACTIVITY_WORKER, LOGGING
from utils.ConsoleProvider import CONSOLE
from workers.base.NonLockingBaseBotWorker import NonLockingBaseBotWorker


class ActivityWorker(NonLockingBaseBotWorker):
    activityContainer: ActivityContainer
    lastUpdateTime: float
    secsBetweenUpdates: float = ACTIVITY_WORKER.secsBetweenUpdates

    def __init__(self, activityContainer: ActivityContainer):
        super().__init__()
        self.activityContainer = activityContainer

    def preInit(self) -> None:
        self.lastUpdateTime = time()

    def hasWork(self) -> bool:
        return (time() - self.lastUpdateTime) > self.secsBetweenUpdates

    def doWork(self) -> None:
        if LOGGING.logUpdatingActivities:
            CONSOLE.print("Updating activities ({})...".format(self.activityContainer.size()))
        self.activityContainer.updateAll()
        self.lastUpdateTime = time()
