LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "yENZawrGJVq3eqQdPo2JzTlUt7YfbxR%2FQynvFStMNmXsAJyqm7ILtc3HRrZTeUt3bCp6tFb2DK4gHsAdwfqJZg%3D%3D%7CmZjdpEppwXyGdmmEJb9ERQ4KHK8V9LZrv6nnwKT8jhgJbltrU9waWYHOSLAUMS%2BVRNQNBniL4uxd8Te8xpFKJA%3D%3D",
    "connect.sid": "s%3A1kdC_Wk2Fmdtq75hO7n3u6fmxSxXQcyd.h%2FHlceueScRGsFEwOFdCRf0SKPQSO1sM8Xs9ua9mpe4"
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
