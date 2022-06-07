from .cmd_exec import CommandExecutor
from .exception import ExitSignal
from structure.singleton import SingletonMeta


class CommandParser(metaclass=SingletonMeta):
    def __init__(self):
        super(CommandParser, self).__init__()

    def input(self):
        s = input("VT>> ")
        lo = s.lower()

        if lo == "exit" or lo == "stop" or lo == "quit":
            return self.__do_exit()

        args = s.split(" ")
        cmd_name = args[0]
        cmd_args = args[1:]
        CommandExecutor().handle_command(cmd_name, *cmd_args)

    def __do_exit(self):
        raise ExitSignal
