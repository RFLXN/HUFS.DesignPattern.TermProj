import sys

from .cmd_exec import CommandExecutor
from .exception import ExitSignal
from structure.singleton import SingletonMeta
from sys import argv, exit


class CommandParser(metaclass=SingletonMeta):
    def __init__(self):
        super(CommandParser, self).__init__()

    def run(self):
        if len(argv) == 1:
            while True:
                try:
                    self.__input()
                except ExitSignal:
                    print("Exit VT.")
                    exit(0)

        args = argv[1:]
        self.__do_instant(*args)

    def __input(self):
        s = input("VT>> ")
        lo = s.lower()

        if lo == "exit" or lo == "stop" or lo == "quit":
            return self.__do_exit()

        args = s.split(" ")
        self.__handle_cmd(*args)

    def __handle_cmd(self, *args, **kwargs):
        cmd_name = args[0]
        cmd_args = args[1:]
        CommandExecutor().handle_command(cmd_name, *cmd_args, **kwargs)

    def __do_exit(self):
        raise ExitSignal

    def __do_instant(self, *args):
        self.__handle_cmd(*args)
