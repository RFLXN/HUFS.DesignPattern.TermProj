from command import Command
from command.result import CommandResult


class AnalysisCommand(Command):
    def __init__(self):
        super(AnalysisCommand, self).__init__()

    def execute(self, *args, **kwargs) -> CommandResult:
        pass
