from properties import MESSAGE_LEN_LIMITS

NEXT_LINE_SYMBOL = "-"


class ChatMessagePreprocessor:
    @staticmethod
    def prepareMessageForGlobal(message: str) -> list[str]:
        limit = MESSAGE_LEN_LIMITS["global"]
        prefix = "/s   "

        return ChatMessagePreprocessor.splitMessageAndAddPrefix(message, prefix, limit)

    @staticmethod
    def prepareMessageForWhisper(message: str, user: str) -> list[str]:
        limit = MESSAGE_LEN_LIMITS["whisper"]
        prefix = "/w {}   ".format(user)

        return ChatMessagePreprocessor.splitMessageAndAddPrefix(message, prefix, limit)

    @staticmethod
    def splitMessageAndAddPrefix(message: str, prefix: str, limit: int) -> list[str]:
        resultMessages = []
        remainingMessage = message
        while len(remainingMessage) > limit:
            partToSend = remainingMessage[: limit + 1]
            resultMessages.append(partToSend)
            # Everything after 'partToSend' is remaining:
            remainingMessage = NEXT_LINE_SYMBOL + remainingMessage[limit + 1:]
        resultMessages.append(remainingMessage)
        resultMessages[0] = prefix + resultMessages[0]
        return resultMessages
