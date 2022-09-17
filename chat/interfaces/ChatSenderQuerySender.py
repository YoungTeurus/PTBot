from chat.ChatMessage import ChatMessage
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory


class ChatSenderQuerySender:
    def addGlobalMessage(self, msg: str, ocmf: OutgoingChatMessageFactory) -> None:
        """
        Преобразует сообщение в глобальное и добавляет сообщение в очередь на отправку.
        """
        self.addMessage(ocmf.globalMsg(msg))

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
        :return:
        """
        raise NotImplementedError
