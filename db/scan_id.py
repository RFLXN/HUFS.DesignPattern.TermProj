from os.path import dirname, realpath
from pathlib import Path
from shutil import copyfile
from datetime import datetime
from structure.singleton import SingletonMeta
from util.json import load_json_from_file, write_json_to_file


def _get_resource_path() -> str:
    return str((Path(dirname(realpath(__file__))) / ".." / "resource").resolve())


def _get_default_db_file_path() -> str:
    return str((Path(_get_resource_path()) / "scan-id.default.json").resolve())


def _get_db_file_path() -> str:
    return str((Path(_get_resource_path()) / "scan-id.json").resolve())


def _cp_db_file():
    copyfile(_get_default_db_file_path(), _get_db_file_path())


class ScanId:
    def __init__(self, scan_id: str, file_path: str, date: datetime):
        self.__scan_id = scan_id
        self.__date = date
        self.__file_path = file_path

    @property
    def scan_id(self) -> str:
        return self.__scan_id

    @property
    def file_path(self) -> str:
        return self.__file_path

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def date_str(self) -> str:
        return self.date.strftime("%Y-%m-%d %H:%M:%S")

    def dictify(self) -> dict:
        return {"id": self.scan_id, "path": self.file_path, "date": self.date_str}


class ScanIdDB(metaclass=SingletonMeta):
    def __init__(self):
        super(ScanIdDB, self).__init__()
        self.__ids: list[ScanId] = []
        self.__load_ids()

    @property
    def id_list(self) -> list[ScanId]:
        self.__sort()
        return self.__ids

    @property
    def last(self) -> ScanId | None:
        self.__sort()
        if len(self.id_list) < 1:
            return None
        return self.id_list[0]

    def add_scan_id(self, scan_id: str, file_path: str):
        id_obj = ScanId(scan_id, file_path, datetime.now())
        self.__ids.append(id_obj)
        self.__save_ids()

    def __sort(self):
        self.__ids.sort(key=lambda id_obj: id_obj.date)

    def __is_db_file_exist(self) -> bool:
        try:
            load_json_from_file(_get_db_file_path())
            return True
        except:
            return False

    def __load_ids(self):
        if not self.__is_db_file_exist():
            print("Initializing Scan ID DB File...")
            _cp_db_file()
        raw_ids = load_json_from_file(_get_db_file_path())
        for raw in raw_ids:
            self.__ids.append(ScanId(raw["id"], raw["path"], datetime.strptime(raw["date"], "%Y-%m-%d %H:%M:%S")))

    def __save_ids(self):
        dict_list = []
        for id_obj in self.__ids:
            dict_list.append(id_obj.dictify())
        write_json_to_file(dict_list, _get_db_file_path())
