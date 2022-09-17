# Никнейм бота в логах до момента определения ника
# Одновременно является ником бота для LOCAL_MODE!
DEFAULT_LOG_BOT_NICKNAME = "BOT"

# Set to True to disable logging in game
LOCAL_MODE = True

LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "diey8s3nwcg8ztS2n09jCF0kuTgSe4oxzoup24upfcv%2BJs%2Bdfahj6n3FO1qlOWyEU49LESGP2xiRWL8iRA%2FWEg%3D%3D%7Cufe%2BPGkD8IGKyG58QO4b0pg5kbGM9uG7DWbHZ62aGmHisUMuqD%2BAltJJk3hWywJIb0aegMMlOFAzZTwUHMB%2FDw%3D%3D",
    "connect.sid": "s%3A0UmnX5wFZ99S2EmFzcSWqUxYZGt86kTv.lxujl7Jw30S%2F%2FL8%2FyPbPdqt%2Fl35zf9o%2BtqhzMJctyGE"
}

WAIT_SETTINGS: dict[str, float] = {
    "timeout": 2,
    "pollFrequency": 0.5
}

GAME_LOAD_WAIT_SETTINGS: dict[str, float] = {
    "timeout": 10,
    "pollFrequency": 1
}

PONY_TOWN_URL: str = "http://pony.town"
PATH_TO_CHROME_DRIVER: str = "./extra/chromedriver.exe"
PATH_TO_FIREFOX_DRIVER: str = "./extra/geckodriver.exe"


class MESSAGE_LEN_LIMITS:
    globalChat: int = 72
    whisperChat: int = 128


CHAT_SENDER_WORKER = {
    "secsBetweenMessages": 1
}

CHAT_READER_WORKER = {
    "secsBetweenChecks": 1
}


class ACTIVITY_WORKER:
    secsBetweenUpdates: float = 5


COMMAND_PREFIX = "!"
SELF_IDENTIFY_MESSAGE_LENGTH = 10


class LOGGING:
    logWorkers: bool = False
