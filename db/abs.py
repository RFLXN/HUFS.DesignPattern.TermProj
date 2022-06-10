from abc import abstractmethod

from structure.singleton import SingletonABCMeta


class AbstractIdDB(metaclass=SingletonABCMeta):
    @abstractmethod
    @property
    def id_list(self) -> list:
        pass

    @abstractmethod
    @property
    def last(self):
        pass

    @abstractmethod
    def add_id(self, i: str, target: str):
        pass
