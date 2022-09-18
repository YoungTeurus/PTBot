# Никнейм бота в логах до момента определения ника
# Одновременно является ником бота для LOCAL_MODE!
DEFAULT_LOG_BOT_NICKNAME = "BOT"

# При установке в True включается Offline мод с работой бота без подключения к игре
LOCAL_MODE = False

LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "iY%2ForMChgfT2quB3cSPLH0sQxrpgJH2AZxwubKQCkM9iYhMhnbOe%2B5dhZXSiw5P9uHay1JnXaOZOfBAyW8vZ0g%3D%3D%7CX4n8llUY6pxq9pOZ5%2FcfsGXZ71ciUo4f96tH2VR%2BD0cESz4%2BL6xmQrf%2BbtvF%2FihzmGfmhj2W01QV45bcAfMMlw%3D%3D",
    "connect.sid": "s%3AV5h5h1DLjhgTetmGEb3KOm4cnx6so_jp.HsJbiunBZnCfs0U3B2rwVaasTmx7%2F7q59BgY%2BWN%2FY1A"
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


BOT_INPUT_PREFIX = "BOT << "

# Список ников, по умолчанию добавляемых в админы.
# НЕБЕЗОПАСНО!
START_UP_ADMINS: list[str] = ["- Teurus [and Fyaf] -"]
