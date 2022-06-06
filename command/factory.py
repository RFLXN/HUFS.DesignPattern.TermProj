from command.abs import Command
from command.real import CommandIndex
from structure.singleton import SingletonMeta


class CommandFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.__commands = dict()
        self.__load_cmd()

    def __load_cmd(self):
        idx = CommandIndex().index
        for cmd_name in idx.keys():
            cmd = idx[cmd_name]
            self.set_command(cmd_name, cmd())

    def get_command(self, command_name: str) -> Command:
        return self.__commands[command_name]

    def __getitem__(self, item: str) -> Command:
        return self.get_command(item)

    def set_command(self, name: str, cmd: Command):
        self.__commands[name] = cmd
