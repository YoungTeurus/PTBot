import time
from typing import Callable, Optional

from chat.ChatMessage import ChatMessage
from utils.Utils import CALLBACK_FUNCTION

# (chat_message) => remove_wait
# Если возвращает True - ожидание ответа удаляется, иначе - продолжаем ждать ответа.
WAIT_MESSAGE_PROCESSOR = Callable[[ChatMessage], bool]


class WaitMessageSettings:
    # Время начала ожидания
    startWaitTime: float
    # Время ожидания ответа в секундах
    timeoutSecs: float
    # Функция, которой передаётся содержимое сообщения
    onCommand: WAIT_MESSAGE_PROCESSOR
    # Вызывается по истечению timeout
    onTimeout: Optional[CALLBACK_FUNCTION]

    def __init__(self, timeoutSecs: float,
                 onCommand: WAIT_MESSAGE_PROCESSOR,
                 onTimeout: Optional[CALLBACK_FUNCTION] = None) -> None:
        self.startWaitTime = time.time()
        self.timeoutSecs = timeoutSecs
        self.onCommand = onCommand
        self.onTimeout = onTimeout
