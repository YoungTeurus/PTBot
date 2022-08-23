LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "w5kQUD%2FNlYvg9DfjfOifGUpGD2wt%2FDng%2FL0kF5Vdz%2FxGYaA12KWyAQBA%2FoGUSKUJFJT7%2BD27h0E%2FQOLIQGflyw%3D%3D%7CoRZ6%2BJhNYH%2F%2B0c64Vg50cN%2FsMEqBrhk8ku%2B%2BtSX465sXSn%2BWA3NUQ1olkgF8OYYQxU1Dz40UegTEZJ1rq68eqQ%3D%3D",
    "connect.sid": "s%3AFJ4JWi8sOzrO7MVMTjEVYYFtv4Y1Z_D0.wUniigKa91KHEiEGtxTmg5KTqs7myuywV1uDRl64BoM"
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
