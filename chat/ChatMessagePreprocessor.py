from properties import MESSAGE_LEN_LIMITS


class ChatMessagePreprocessor:
    @staticmethod
    def prepareMessageForGlobal(message: str) -> list[str]:
        limit = MESSAGE_LEN_LIMITS["global"]
        prefix = "/s "

        return ChatMessagePreprocessor.splitMessageAndAddPrefix(message, prefix, limit)

    @staticmethod
    def prepareMessageForWhisper(message: str, user: str) -> list[str]:
        limit = MESSAGE_LEN_LIMITS["whisper"]
        prefix = "/w {} ".format(user)

        return ChatMessagePreprocessor.splitMessageAndAddPrefix(message, prefix, limit)

    @staticmethod
    def splitMessageAndAddPrefix(message: str, prefix: str, limit: int) -> list[str]:
        resultMessages = []
        parts = len(message) // limit
        for i in range(parts + 1):
            resultMessages.append(message[limit * i: limit * (i + 1)])
        resultMessages[0] = prefix + resultMessages[0]
        return resultMessages
