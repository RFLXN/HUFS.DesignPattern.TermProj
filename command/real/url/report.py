from command import Command
from command.result import CommandResult


class ReportCommand(Command):
    def __init__(self):
        super(ReportCommand, self).__init__()
        self._name = "url-report"

    def _execute(self, *args) -> CommandResult:
        pass

    def help(self) -> str:
        pass

