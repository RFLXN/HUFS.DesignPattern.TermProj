class FileStatus:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def raw(self) -> dict[str, int]:
        return self.__raw

    @property
    def harmless(self) -> int:
        return self.raw["harmless"]

    @property
    def type_unsupported(self) -> int:
        return self.raw["type-unsupported"]

    @property
    def suspicious(self) -> int:
        return self.raw["suspicious"]

    @property
    def timeout(self) -> int:
        return self.raw["timeout"]

    @property
    def failure(self) -> int:
        return self.raw["failure"]

    @property
    def malicious(self) -> int:
        return self.raw["malicious"]

    @property
    def undetected(self) -> int:
        return self.raw["undetected"]


class FileScanResult:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def raw(self) -> dict[str, str]:
        return self.__raw

    @property
    def result(self) -> str:
        return self.raw["category"]

    @property
    def engine_name(self) -> str:
        return self.raw["engine_name"]

    @property
    def engine_version(self) -> str:
        return self.raw["engine_version"]


class FileReport:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def raw(self) -> dict:
        return self.__raw["data"]

    @property
    def attr(self) -> dict:
        return self.raw["attributes"]

    @property
    def file_id(self) -> str:
        return self.raw["id"]

    @property
    def file_type(self) -> str:
        return self.attr["type_description"]

    @property
    def file_name(self) -> str:
        return self.attr["names"][0]

    @property
    def file_size(self) -> int:
        return self.attr["size"]

    @property
    def file_extension(self) -> str:
        return self.attr["type_extension"]

    @property
    def file_status(self) -> FileStatus:
        return FileStatus(self.attr["last_analysis_stats"])

    @property
    def scaner_names(self) -> list[str]:
        return self.attr["last_analysis_results"].keys()

    @property
    def raw_scan_results(self) -> dict[str, dict[str, str]]:
        return self.attr["last_analysis_results"]

    def get_scan_result(self, scaner_name: str):
        return FileScanResult(self.raw_scan_results[scaner_name])
