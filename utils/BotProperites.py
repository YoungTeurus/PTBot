from enum import Enum
from typing import Optional


class BotState(Enum):
    STARTING = 1
    INITIALIZED = 2

class BotProperties:
    botName: Optional[str]
    state: BotState
    admins: list[str]

    def __init__(self):
        self.botName = None
        self.state = BotState.STARTING
        self.admins = []
