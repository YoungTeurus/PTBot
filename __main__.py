from time import sleep

from Bot import createAndInitBot, Bot
from modules.commands.AddAdminCommandModule import AddAdminCommandModule
from modules.commands.LobbyCreator import LobbyCreator
from modules.commands.Recorder import Recorder
from modules.commands.SwitchableParrot import SwitchableParrot
from modules.console.ConsoleToBotSender import ConsoleToBotSender
from modules.console.ConsoleToChatSender import ConsoleToChatSender
from properties import LOCAL_MODE
from utils.ConsoleProvider import CONSOLE
from workers.InputFromConsoleWorker import InputFromConsoleWorker


def loadCustomModules(_bot: Bot) -> None:
    CONSOLE.print("Loading custom modules (observers)...")
    ifcw = InputFromConsoleWorker(_bot.cc)
    _bot.bwc.add(ifcw)

    _bot.cc.addCommands(ConsoleToBotSender(_bot.bp, _bot.icmp, _bot.cprovide)._getConsoleCommands())
    _bot.cc.addCommands(ConsoleToChatSender(_bot.csqs, _bot.ocmf)._getConsoleCommands())

    _bot.cprovide.addObserver(SwitchableParrot(_bot.csqs, _bot.ocmf))
    _bot.cprovide.addObserver(Recorder(_bot.csqs, _bot.ocmf))
    aacm = AddAdminCommandModule(_bot.csqs, _bot.ocmf, _bot.bp)
    _bot.cc.addCommands(aacm._getConsoleCommands())
    _bot.cprovide.addObserver(aacm)

    _bot.cprovide.addObserver(LobbyCreator(_bot.csqs, _bot.ocmf, _bot.bp))

    CONSOLE.print("Finished loading custom modules!")


if __name__ == "__main__":
    CONSOLE.print("Starting bot...")

    bot: Bot = createAndInitBot(LOCAL_MODE, loadCustomModules)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        bot.bwc.stopAll()
