# Никнейм бота в логах до момента определения ника
# Одновременно является ником бота для LOCAL_MODE!
DEFAULT_LOG_BOT_NICKNAME = "BOT"

# При установке в True включается Offline мод с работой бота без подключения к игре
LOCAL_MODE = True

LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "80YA33jPU4uq4ToixAJ2u8kBlztqpL7eQIKdBiz9t1LpPX78dQVcwoUJ9xRBdoBkkPvrLeMmhTa%2FVDVgrzjqnw%3D%3D%7C5lyr8VE0sDCEFV6543sELwurfBKvCqZANuuUKHUkhYFN1xCnqQJN%2FLwnxWHnn9Zoujxyft20OYty0n9zD4ekvQ%3D%3D",
    "connect.sid": "s%3A_bN_fVJAFCyE5dZhdclNkNGsP5g6zx0I.fgfUzofQipWNbv%2FjwPC7bYABODwCa78JxWFkFzqzgvU"
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


# Определяет символ(-ы), необходимые для установки перед сообщением, чтобы бот распознал в них команду.
COMMAND_PREFIX = "!"


SELF_IDENTIFY_MESSAGE_LENGTH = 10


class LOGGING:
    logWorkers: bool = False
    logUpdatingActivities: bool = False


class ArgsDevider:
    quotationMark: str = '"'
