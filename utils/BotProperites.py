from enum import Enum


class BotState(Enum):
    STARTING = 1
    INITIALIZED = 2

class BotProperties:
    botName: str | None
    state: BotState

    def __init__(self):
        self.botName = None
        self.state = BotState.STARTING
