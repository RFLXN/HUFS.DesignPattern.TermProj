class CommandResult:
    def __init__(self, success: bool, msg: str):
        self.__success = success
        self.__msg = msg

    @property
    def success(self) -> bool:
        return self.__success

    @property
    def result(self) -> str:
        return self.__msg
