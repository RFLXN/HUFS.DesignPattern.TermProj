from .abs import Command
from .exception import InvalidCommandException
from .real import CommandIndex
from structure.singleton import SingletonMeta


class CommandFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.__commands: list[Command] = []
        self.__load_cmd()

    def __load_cmd(self):
        idx = CommandIndex().index
        for command in idx:
            self.__commands.append(command())

    def get_command(self, command_name: str) -> Command:
        for cmd in self.__commands:
            if cmd.name.lower() == command_name.lower():
                return cmd
        raise InvalidCommandException

    def __getitem__(self, item: str) -> Command:
        return self.get_command(item)
