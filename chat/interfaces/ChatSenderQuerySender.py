from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory


class ChatSenderQuerySender:
    def addGlobalMessage(self, msg: str, ocmf: OutgoingChatMessageFactory) -> None:
        """
        Преобразует сообщение в глобальное и добавляет сообщение в очередь на отправку.
        """
        self.addMessage(ocmf.globalMsg(msg))

    def addWhisperMessage(self, msg: str, receiver: str, ocmf: OutgoingChatMessageFactory) -> None:
        self.addMessage(ocmf.whisperMsg(msg, receiver))

    def addMessages(self, msgs: list[ChatMessage]) -> None:
        for msg in msgs:
            self.addMessage(msg)

    def addMessage(self, msg: ChatMessage) -> None:
        """
        Добавляет сообщение в очередь на отправку.
        """
        raise NotImplementedError

    def sendNextMessage(self) -> None:
        """
        Отправляет следующее сообщение в очереди в игровой чат.
        """
        raise NotImplementedError

    def hasMsgs(self) -> bool:
        """
        Возвращает True, если хотя бы одно сообщение находится в очереди на отправку.
        """
        raise NotImplementedError

    def cleanMsgQueue(self) -> None:
        """
        Очищает очередь сообщений для отправки
        """
        raise NotImplementedError
