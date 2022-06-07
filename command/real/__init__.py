from structure.singleton import SingletonMeta
from .key import KeyCommand


class CommandIndex(metaclass=SingletonMeta):
    def __init__(self):
        import files
        import analysis
        super(CommandIndex, self).__init__()
        self.__idx = {
            "scan-file": files.ScanCommand,
            "analysis": analysis.AnalysisCommand,
            "key": KeyCommand
        }

    @property
    def index(self) -> dict:
        return self.__idx
