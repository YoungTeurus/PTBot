from chat.ChatMessage import ChatMessage
from chat.ChatSenderQuerySender import ChatSenderQuerySender
from modules.base.CommandDrivenModule import CommandDrivenModule, ACTION_CALLBACK, ChatCommand, ChatCommandArg


class TestCommandModule(CommandDrivenModule):
    csqs: ChatSenderQuerySender

    def __init__(self, csqs: ChatSenderQuerySender):
        super().__init__()
        self.csqs = csqs

        args = [
            ChatCommandArg("text")
        ]

        command: ChatCommand = ChatCommand("test", self.sayFirstArg, args)

        self.addCommand(command)

    def sayFirstArg(self, msg: ChatMessage, args: list[str]) -> None:
        textToSay = args[0]
        print("Command 'test' with argument '{}'".format(textToSay))
        self.csqs.addMessageToQuery("Повторяю: '{}'".format(textToSay))

