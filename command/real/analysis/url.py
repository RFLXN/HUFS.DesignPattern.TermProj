class UrlStatusWrapper:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def raw(self) -> dict:
        return self.__raw

    @property
    def harmless(self) -> str:
        return self.raw["harmless"]

    @property
    def malicious(self) -> str:
        return self.raw["malicious"]

    @property
    def suspicious(self) -> str:
        return self.raw["suspicious"]

    @property
    def undetected(self) -> str:
        return self.raw["undetected"]

    @property
    def timeout(self) -> str:
        return self.raw["timeout"]


class UrlScanEngineResultWrapper:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def raw(self) -> dict:
        return self.__raw

    @property
    def result(self) -> str:
        return self.raw["category"]

    @property
    def engine_name(self) -> str:
        return self.raw["engine_name"]


class UrlAnalysisResultWrapper:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def raw(self) -> dict:
        return self.__raw

    @property
    def attr(self) -> dict:
        return self.__raw["attributes"]

    @property
    def progress(self):
        return self.attr["status"]

    @property
    def status(self) -> UrlStatusWrapper:
        return UrlStatusWrapper(self.attr["stats"])

    @property
    def scaner_names(self):
        return self.attr["results"].keys()

    @property
    def scan_results(self) -> dict[str, UrlScanEngineResultWrapper]:
        raw_results = self.attr["results"]
        results = {}

        for scaner_name in self.scaner_names:
            results[scaner_name] = UrlScanEngineResultWrapper(raw_results[scaner_name])

        return results

    @property
    def scan_id(self) -> str:
        return self.raw["id"]


def do_url_default(result: UrlAnalysisResultWrapper) -> str:
    pass


def do_url_verbose(result: UrlAnalysisResultWrapper) -> str:
    pass
