from chat.ChatMessage import ChatMessage
from properties import MESSAGE_LEN_LIMITS

NEXT_LINE_SYMBOL = "-"


class OutgoingChatMessagePreprocessor:
    @staticmethod
    def prepareMessage(message: ChatMessage) -> list[str]:
        """
        Преобразует объект ChatMessage в набор строк для отправки в чат.
        Использует:
        * message.body для определения содержимого сообщения,
        * message.receiver для определения адресата (если указан - сообщение будет отправлено как шёпот)
        :param message:
        :return:
        """
        if message.receiver is None:
            return OutgoingChatMessagePreprocessor.prepareMessageForGlobal(message.body)
        else:
            return OutgoingChatMessagePreprocessor.prepareMessageForWhisper(message.body, message.receiver)

    @staticmethod
    def prepareMessageForGlobal(message: str) -> list[str]:
        limit = MESSAGE_LEN_LIMITS.globalChat
        prefix = "/s   "

        return OutgoingChatMessagePreprocessor.splitMessageAndAddPrefix(message, prefix, limit)

    @staticmethod
    def prepareMessageForWhisper(message: str, user: str) -> list[str]:
        limit = MESSAGE_LEN_LIMITS.whisperChat
        prefix = "/w {}   ".format(user)

        return OutgoingChatMessagePreprocessor.splitMessageAndAddPrefix(message, prefix, limit)

    @staticmethod
    def splitMessageAndAddPrefix(message: str, prefix: str, limit: int) -> list[str]:
        resultMessages = []
        remainingMessage = message
        while len(remainingMessage) > limit:
            partToSend = remainingMessage[: limit + 1]
            resultMessages.append(partToSend)
            # Всё после 'partToSend' остаётся:
            remainingMessage = NEXT_LINE_SYMBOL + remainingMessage[limit + 1:]
        resultMessages.append(remainingMessage)
        resultMessages[0] = prefix + resultMessages[0]
        return resultMessages
