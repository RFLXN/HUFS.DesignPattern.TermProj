from structure.singleton import SingletonMeta


class CommandIndex(metaclass=SingletonMeta):
    def __init__(self):
        from .analysis import AnalysisCommand
        from .files import ScanCommand
        from .key import KeyCommand
        super(CommandIndex, self).__init__()
        self.__idx = [ScanCommand, AnalysisCommand, KeyCommand]

    @property
    def index(self) -> list:
        return self.__idx
