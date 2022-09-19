from modules.base.Command import ARGS_DICT, Command, CommandArg
from modules.base.OutputtingCommandDrivenModule import OutputtingCommandDrivenChatObserver
from utils.ConsoleProvider import CONSOLE


class TestCommandModule(OutputtingCommandDrivenChatObserver):

    def _getInitialCommands(self) -> list[Command]:
        return [Command("test", self.sayFirstArg, [CommandArg("text")])]

    def sayFirstArg(self, args: ARGS_DICT) -> None:
        textToSay: str = args["text"]
        CONSOLE.print("Command 'test' with argument '{}'".format(textToSay))
        self.globalMessage("Повторяю: '{}'".format(textToSay))
