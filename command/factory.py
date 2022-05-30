from command.abs import Command
from structure.singleton import SingletonMeta


class CommandFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.__commands = dict()

    def get_command(self, command_name: str) -> Command:
        return self.__commands[command_name]

    def __getitem__(self, item: str) -> Command:
        return self.get_command(item)

    def set_command(self, name: str, cmd: Command):
        self.__commands[name] = cmd
