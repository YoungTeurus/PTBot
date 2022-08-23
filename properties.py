LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "Wq6mNx90RmEMCm8p0oYECV9tFcmLX%2F2hhfc4ky25ijLR1QuQOZGwiK28eIdfyCZjOm1Jg4r9p5w%2BvLcSjV52vA%3D%3D%7C%2BxovLSiDn%2FTjViZ%2BI%2BtsXIZQEfnvnf24jZQVtVtA5gsrP1VA9uqQTcRT7mNObw0kighEbnjvT7kP8dYAErqacg%3D%3D",
    "connect.sid": "s%3A5XIwt8JkaNkRMvtwx6EyEAe9XsWnckA_.%2BM5TKcHINFFXeeBmcKM1sHuZrMZu8PgPNQD0R9hqebk"
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
