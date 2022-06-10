class FileStatusWrapper:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def harmless(self) -> str:
        return self.__raw["harmless"]

    @property
    def unsupported_type(self) -> str:
        return self.__raw["type-unsupported"]

    @property
    def suspicious(self) -> str:
        return self.__raw["suspicious"]

    @property
    def timeout(self) -> str:
        return self.__raw["timeout"]

    @property
    def failure(self) -> str:
        return self.__raw["failure"]

    @property
    def malicious(self) -> str:
        return self.__raw["malicious"]

    @property
    def undetected(self) -> str:
        return self.__raw["undetected"]


class FileScanEngineResultWrapper:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def result(self) -> str:
        return self.__raw["category"]

    @property
    def engine_name(self) -> str:
        return self.__raw["engine_name"]

    @property
    def engine_version(self) -> str:
        return self.__raw["engine_version"]

    @property
    def engine_update(self) -> str:
        return self.__raw["engine_update"]


class FileAnalysisResultWrapper:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def progress(self) -> str:
        return self.__raw["attributes"]["status"]

    @property
    def status(self) -> FileStatusWrapper:
        return FileStatusWrapper(self.__raw["attributes"]["stats"])

    @property
    def vaccine_names(self) -> list[str]:
        return self.__raw["attributes"]["results"].keys()

    @property
    def scan_results(self) -> dict[str, FileScanEngineResultWrapper]:
        results = {}
        raw_results = self.__raw["attributes"]["results"]

        for name in self.vaccine_names:
            result = raw_results[name]
            results[name] = FileScanEngineResultWrapper(result)

        return results

    @property
    def scan_id(self) -> str:
        return self.__raw["id"]


def do_file_default(result: FileAnalysisResultWrapper) -> str:
    msg = f"Progress: {result.progress}\n"
    msg += f"Undetected: {result.status.undetected}\n" \
           + f"Harmless: {result.status.harmless}\n" \
           + f"Malicious: {result.status.malicious}\n" \
           + f"Suspicious: {result.status.suspicious}\n" \
           + f"Failure: {result.status.failure}\n" \
           + f"Timeout: {result.status.timeout}\n" \
           + f"Type Unsupported: {result.status.unsupported_type}\n"

    return msg


def do_file_verbose(result: FileAnalysisResultWrapper) -> str:
    msg = do_file_default(result)

    for vaccine_name in result.vaccine_names:
        vaccine_result = result.scan_results[vaccine_name]
        msg += f"\n{vaccine_result.engine_name} ({vaccine_result.engine_version}): {vaccine_result.result}"

    return msg
