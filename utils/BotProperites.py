from enum import Enum
from typing import Optional

from properties import START_UP_ADMINS


class BotState(Enum):
    STARTING = 1
    ENTERED_GAME = 2
    INITIALIZED = 3


class BotProperties:
    botName: Optional[str]
    state: BotState
    admins: list[str]

    def __init__(self):
        self.botName = None
        self.state = BotState.STARTING
        self.admins = START_UP_ADMINS
