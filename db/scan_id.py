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
    def __init__(self, scan_id: str, object_id: str, scan_target: str, target_type: str, date: datetime):
        self.__scan_id = scan_id
        self.__date = date
        self.__scan_target = scan_target
        self.__object_id = object_id
        self.__target_type = target_type

    @property
    def scan_id(self) -> str:
        return self.__scan_id

    @property
    def scan_target(self) -> str:
        return self.__scan_target

    @property
    def object_id(self) -> str:
        return self.__object_id

    @property
    def target_type(self) -> str:
        return self.__target_type

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def date_str(self) -> str:
        return self.date.strftime("%Y-%m-%d %H:%M:%S")

    def dictify(self) -> dict:
        return {"scan_id": self.scan_id,
                "object_id": self.object_id,
                "target": self.scan_target,
                "type": self.target_type,
                "date": self.date_str}


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

    def add_id(self, scan_id: str, object_id: str, target: str, target_type: str):
        id_obj = ScanId(scan_id, object_id, target, target_type, datetime.now())
        self.__ids.append(id_obj)
        self.__save_ids()

    def __sort(self):
        self.__ids.sort(key=lambda id_obj: id_obj.date, reverse=True)

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
            self.__ids.append(
                ScanId(raw["scan_id"],
                       raw["object_id"],
                       raw["target"],
                       raw["type"],
                       datetime.strptime(raw["date"], "%Y-%m-%d %H:%M:%S"))
            )

    def __save_ids(self):
        dict_list = []
        for id_obj in self.__ids:
            dict_list.append(id_obj.dictify())
        write_json_to_file(dict_list, _get_db_file_path())
