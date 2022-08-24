LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "bnhvmbvu4z8zhspdWErSRzkhjthGrrNhFbjW5e8%2BX2WIYcVRaTaJ4L4pFqQK1iH6AwvwC0qnYo5v5oArolWtVg%3D%3D%7CprfQQBms4wHJVkjU0MkU6OSdcsq0oZrlsTg2TJ9JUWV41Vjxrle8UwicjEAUzO15wqrvyHRYmXZbyrOp4%2Bkd8g%3D%3D",
    "connect.sid": "s%3A5Vzusjv9xqm4N_hAgo5fOXl2GLs-W620.ilcN4%2FHELZlnBVhblHgBTh%2Faa5VfMaYsE574BClICJI"
}

WAIT_SETTINGS: dict[str, float] = {
    "timeout": 2,
    "pollFrequency": 0.5
}

PONY_TOWN_URL: str = "http://pony.town"
PATH_TO_CHROME_DRIVER: str = "./extra/chromedriver.exe"
PATH_TO_FIREFOX_DRIVER: str = "./extra/geckodriver.exe"

MESSAGE_LEN_LIMITS: dict[str, int] = {
    "global": 72,
    "whisper": 128
}

CHAT_SENDER_WORKER = {
    "secsBetweenMessages": 1
}

CHAT_READER_WORKER = {
    "secsBetweenChecks": 1
}

COMMAND_PREFIX = "!"
SELF_IDENTIFY_MESSAGE_LENGTH = 10
