class BotProperties:
    botName: str | None
    loggedIn: bool

    def __init__(self):
        self.botName = None
        self.loggedIn = False
