from chat.ChatMessage import ChatMessage
from chat.GameChatSenderQuerySender import GameChatSenderQuerySender
from modules.base.CommandDrivenModule import CommandDrivenModule, ChatCommand, ChatCommandArg


class TestCommandModule(CommandDrivenModule):
    csqs: GameChatSenderQuerySender

    def __init__(self, csqs: GameChatSenderQuerySender):
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
        self.csqs.addMessage("Повторяю: '{}'".format(textToSay))

