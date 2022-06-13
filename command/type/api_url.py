class UrlStatus:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def raw(self) -> dict:
        return self.__raw

    @property
    def harmless(self) -> int:
        return self.raw["harmless"]

    @property
    def malicious(self) -> int:
        return self.raw["malicious"]

    @property
    def suspicious(self) -> int:
        return self.raw["suspicious"]

    @property
    def undetected(self) -> int:
        return self.raw["undetected"]

    @property
    def timeout(self) -> int:
        return self.raw["timeout"]


class UrlScanResult:
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


class UrlReport:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def raw(self) -> dict:
        return self.__raw["data"]

    @property
    def attr(self) -> dict:
        return self.raw["attributes"]

    @property
    def url_id(self) -> str:
        return self.raw["id"]

    @property
    def url(self) -> str:
        return self.attr["url"]

    @property
    def page_title(self) -> str:
        return self.attr["title"]

    @property
    def category_analyse_engine_names(self) -> list[str]:
        return self.attr["categories"].keys()

    @property
    def raw_category_analyses(self) -> dict[str, str]:
        return self.attr["categories"]

    def get_category_analyse(self, category_engine: str) -> str:
        return self.raw_category_analyses[category_engine]

    @property
    def status(self) -> UrlStatus:
        return UrlStatus(self.attr["last_analysis_stats"])

    @property
    def scaner_names(self) -> list[str]:
        return self.attr["last_analysis_results"].keys()

    @property
    def raw_scan_result(self) -> dict[str, dict[str, str]]:
        return self.attr["last_analysis_results"]

    def get_scan_result(self, scaner_name: str) -> UrlScanResult:
        return UrlScanResult(self.raw_scan_result[scaner_name])
