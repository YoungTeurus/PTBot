from chat.ChatMessage import ChatMessage
from chat.GameChatSenderQuerySender import GameChatSenderQuerySender
from chat.OutgoingChatMessageFactory import OutgoingChatMessageFactory
from modules.base.CommandDrivenModule import CommandDrivenModule, Command, CommandArg
from utils.ConsoleProvider import ConsoleProvider


class TestCommandModule(CommandDrivenModule):
    csqs: GameChatSenderQuerySender
    ocmf: OutgoingChatMessageFactory

    def __init__(self, csqs: GameChatSenderQuerySender, ocmf: OutgoingChatMessageFactory, cp: ConsoleProvider):
        super().__init__(cp)
        self.csqs = csqs
        self.ocmf = ocmf

        args = [
            CommandArg("text")
        ]

        command: Command = Command("test", self.sayFirstArg, args)

        self.addCommand(command)

    def sayFirstArg(self, msg: ChatMessage, args: list[str]) -> None:
        textToSay = args[0]
        self.cp.print("Command 'test' with argument '{}'".format(textToSay))
        self.csqs.addGlobalMessage("Повторяю: '{}'".format(textToSay), self.ocmf)

