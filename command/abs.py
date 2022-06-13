from abc import ABCMeta, abstractmethod

from .exception import InvalidArgumentException
from .result import CommandResult


class Command(metaclass=ABCMeta):
    def __init__(self):
        self._name = ""

    def run(self, *args) -> CommandResult:
        pre = self._pre_execute(*args)
        if pre is not None:
            return pre
        try:
            return self._execute(*args)
        except InvalidArgumentException:
            return CommandResult(False, "Error: Invalid Argument. type ")

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def _execute(self, *args) -> CommandResult:
        pass

    @abstractmethod
    def help(self) -> str:
        pass

    def _handle_help(self):
        return CommandResult(True, self.help())

    def _pre_execute(self, *args) -> CommandResult | None:
        is_help = False
        if len(args) > 0 and args[0] is not None and args[0].lower() == "help":
            is_help = True

        if is_help:
            return self._handle_help()

    def _has_args(self, length: int, args: None | tuple) -> bool:
        if args is None or len(args) < length or args[length - 1] is None or args[length - 1] == "":
            return False
        return True
