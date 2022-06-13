from command.abs import Command
from structure.singleton import SingletonMeta


class CommandIndex(metaclass=SingletonMeta):
    def __init__(self):
        from .files import ScanCommand as FileScan, ReportCommand as FileReport
        from .key import KeyCommand
        from .help import HelpCommand
        from .ids import IdCommand
        from .url import ScanCommand as UrlScan, ReportCommand as UrlReport
        super(CommandIndex, self).__init__()

        self.__idx = [FileScan, KeyCommand, HelpCommand, IdCommand, UrlScan, FileReport, UrlReport]

    @property
    def index(self) -> list[type(type(Command))]:
        return self.__idx
