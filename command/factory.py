from structure.singleton import SingletonMeta
from .abs import Command
from .exception import InvalidCommandException
from .real import CommandIndex


class CommandFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.__commands: list[Command] = []
        self.__load_cmd()
        self.__sort_cmd()

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

    def __sort_cmd(self):
        self.__commands.sort(key=lambda cmd: cmd.name)

    @property
    def all_commands(self) -> list[Command]:
        return self.__commands
