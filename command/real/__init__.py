from command.abs import Command
from structure.singleton import SingletonMeta


class CommandIndex(metaclass=SingletonMeta):
    def __init__(self):
        from .analysis import AnalysisCommand
        from .files import ScanCommand
        from .key import KeyCommand
        from .help import HelpCommand
        super(CommandIndex, self).__init__()

        self.__idx = [ScanCommand, AnalysisCommand, KeyCommand, HelpCommand]

    @property
    def index(self) -> list[Command]:
        return self.__idx
