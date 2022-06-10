from command.abs import Command
from structure.singleton import SingletonMeta


class CommandIndex(metaclass=SingletonMeta):
    def __init__(self):
        from .analysis import AnalysisCommand
        from .files import ScanCommand as FileScan
        from .key import KeyCommand
        from .help import HelpCommand
        from .ids import IdCommand
        from .url import ScanCommand as UrlScan
        super(CommandIndex, self).__init__()

        self.__idx = [FileScan, AnalysisCommand, KeyCommand, HelpCommand, IdCommand, UrlScan]

    @property
    def index(self) -> list[Command]:
        return self.__idx
