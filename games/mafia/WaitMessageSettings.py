import time
from typing import Callable

from chat.ChatMessage import ChatMessage

# (chat_message) => remove_wait
# Если возвращает True - ожидание ответа удаляется, иначе - продолжаем ждать ответа.
WAIT_MESSAGE_PROCESSOR = Callable[[ChatMessage], bool]
# (nickname) => None
WAIT_MESSAGE_ON_TIMEOUT_CALLBACK = Callable[[str], None]


class WaitMessageSettings:
    # Время начала ожидания
    startWaitTime: float
    # Время ожидания ответа в секундах
    timeoutSecs: float
    # Функция, которой передаётся содержимое сообщения
    onCommand: WAIT_MESSAGE_PROCESSOR
    # Вызывается по истечению timeout
    onTimeout: WAIT_MESSAGE_ON_TIMEOUT_CALLBACK

    def __init__(self, timeoutSecs: float,
                 onCommand: WAIT_MESSAGE_PROCESSOR,
                 onTimeout: WAIT_MESSAGE_ON_TIMEOUT_CALLBACK) -> None:
        self.startWaitTime = time.time()
        self.timeoutSecs = timeoutSecs
        self.onCommand = onCommand
        self.onTimeout = onTimeout
