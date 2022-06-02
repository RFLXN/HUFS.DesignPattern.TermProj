from abc import ABCMeta, abstractmethod

from command.result import CommandResult


class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, *args, **kwargs) -> CommandResult:
        pass
    