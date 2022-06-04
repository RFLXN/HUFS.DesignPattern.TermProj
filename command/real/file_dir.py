from command import Command
from command.exception import InvalidArgumentException
from command.real.analysis.analysis import AnalysisCommand
from command.real.files.scan import ScanCommand
from command.result import CommandResult


class FileCommand(Command):
    def __init__(self):
        super(FileCommand, self).__init__()

    def execute(self, *args, **kwargs) -> CommandResult:
        try:
            cmd_type = ""

            if len(args) >= 1 and args[0] is not None and args[0] != "":
                cmd_type = args[0]

            if kwargs["cmd_type"] is not None and kwargs["cmd_type"] != "":
                cmd_type = kwargs["cmd_type"]

            if cmd_type == "":
                raise InvalidArgumentException

            cmd_type = cmd_type.lower()

            if cmd_type == "scan":
                return ScanCommand().execute(*args, **kwargs)

            return CommandResult(False, "Error: Invalid Command.")

        except InvalidArgumentException:
            return CommandResult(False, "Error: Invalid Argument.")
