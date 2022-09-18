from __future__ import annotations

import datetime

UNKNOWN = "UNKNOWN"
BOT_NAME = "BOT_NAME"
SYSTEM = "SYSTEM"
EVERYONE = "EVERYONE"


class ChatMessageType:
    isSystem: bool
    isWhisper: bool
    isAnnouncement: bool
    isSentByBot: bool
    isSentToBot: bool
    isSentByBotAdmin: bool

    def __init__(self):
        self.isSystem = False
        self.isWhisper = False
        self.isAnnouncement = False
        self.isSentByBot = False
        self.isSentToBot = False
        self.isSentByBotAdmin = False


class ChatMessage:
    type: ChatMessageType
    lead: str
    timestamp: datetime.datetime
    label: str
    sender: str
    receiver: str
    body: str

    def __init__(self, type: ChatMessageType, lead: str, timestamp: datetime.datetime, label: str, sender: str, receiver: str,
                 body: str):
        self.type = type
        self.lead = lead
        self.timestamp = timestamp
        self.label = label
        self.sender = sender
        self.receiver = receiver
        self.body = body

    def __str__(self):
        flags = ""
        sender = None
        if self.type.isSystem:
            sender = SYSTEM
            flags += "s"
        if self.type.isWhisper:
            flags += "w"
        if self.type.isAnnouncement:
            sender = SYSTEM
            flags += "a"
        if len(flags) < 1:
            flags += "n"

        sender = self.sender if sender is None else sender
        if self.type.isSentByBotAdmin:
            sender = sender + "(ADMIN)"
        receiver = EVERYONE if self.receiver is None else self.receiver

        return "{} {} {} -> {}: {}".format(flags, self.timestamp.strftime("%H:%M"), sender, receiver, self.body)

    class Builder:
        type: ChatMessageType
        lead: str = None
        timestamp: datetime.datetime
        label: str = None
        sender: str = None
        receiver: str = None
        body: str = None

        def __init__(self):
            self.type = ChatMessageType()
            self.timestamp = datetime.datetime.now()

        def build(self) -> ChatMessage:
            return ChatMessage(self.type, self.lead, self.timestamp, self.label, self.sender, self.receiver, self.body)
