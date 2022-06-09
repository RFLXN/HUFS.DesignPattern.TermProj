from command import Command
from command.exception import InvalidCommandException
from command.real import CommandIndex
from command.result import CommandResult


class HelpCommand(Command):
    def __init__(self):
        super(HelpCommand, self).__init__()
        self._name = "help"

    def _execute(self, *args) -> CommandResult:
        if self._has_args(1, args):
            return self.__do_target_help(args[0])
        else:
            return self.__do_default_help()

    def help(self) -> str:
        return "Command: help / Usage: help [COMMAND_NAME]"

    def __do_target_help(self, cmd_name: str) -> CommandResult:
        for cmd in CommandIndex().index:
            target: Command = cmd()
            if target.name.lower() == cmd_name.lower():
                return CommandResult(True, target.help())
        raise InvalidCommandException

    def __do_default_help(self) -> CommandResult:
        msg = ""
        for cmd in CommandIndex().index:
            target: Command = cmd()
            msg += target.help() + "\n"
        msg = msg[:-1]
        return CommandResult(True, msg)
