from utils.ArgsDevider import splitArgs


class CommandParser:
    @staticmethod
    def getCommandAndArgs(body: str) -> tuple[str, list[str]]:
        """
        Разделяет body на команду и список аргументов.
        Команда - первый элемент body, отделённый пробелом.
        :param body: Текст команды вместе с аргументами
        :return: Tuple, первый элемент - команда, второй элемент - список аргументов
        """
        commandAndArgs = splitArgs(body)
        command = commandAndArgs[0]
        args = commandAndArgs[1:]
        return command, args
