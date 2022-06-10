from db.abs import AbstractIdDB
from structure.singleton import SingletonMeta


class UrlID:
    pass


class UrlIdDB(AbstractIdDB):
    metaclass = SingletonMeta

    def __init__(self):
        super(UrlIdDB, self).__init__()
        self.__id_list: list[UrlID] = []

    @property
    def id_list(self) -> list:
        self.__sort()
        return self.__id_list

    @property
    def last(self) -> UrlID | None:
        self.__sort()
        return self.__id_list[0]

    def add_id(self, i: str, target: str):
        pass

    def __sort(self):
        pass
