LOGIN_SETTINGS: dict[str, str] = {
    "remember_me": "30ZVtXQhekI9ptrgNxslR6Y9KQAFABaIn5grlft2%2BI8iInMbGVDarc%2F4Mle6DgN3WKzInqhZVJ6mxHMvvE6vTA%3D%3D%7COamkeuvBZ%2BaqoI70iqSjXy7VOFK4txt%2F2eGVaGs6sE5A1QjPtV57JlOG5eJlexZNRKIACaqsLAgih8qtZPoFdg%3D%3D",
    "connect.sid": "s%3AB0W39nS7jsSYVwKXhXYC1UlL58m5OVp3.OpSpNzaB%2Fs%2FVKHnMzpK43StLBDwJSYfXAGO83UbB5%2F8"
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
