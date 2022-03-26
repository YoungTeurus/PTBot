LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "tGNOKsXL5ARlXpj0uSFsLnZv4OZtF%2B1fCEzmgQMcomLKGJ0FdsNqTkdxrP0uqiSO7gpnzEV4mZpzUAa0GLs7Ew%3D%3D%7Cw4sFlYE45N08M9XheP6ZSTMLwNDq2747T%2FLJPpAkbq8vh2MDc3D8xYDIELOltwJ6uPKs9FHspjJD2AEd%2FToViA%3D%3D",
    "connect.sid": "s%3AWhJY5BlhdOZQ54I-0lVnOmGm8B3p65ob.dqicy9S63ZHT8f0dqM2KIYbiZhPkvtnr9zB4%2Bgk2X98"
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
