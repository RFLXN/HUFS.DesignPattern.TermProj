from api import ApiClient
from command import Command
from command.exception import InvalidArgumentException, InvalidApiKeyException
from command.result import CommandResult
from util.json import load_json_from_str
from db import ScanIdDB


class StatusWrapper:
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


class VaccineResultWrapper:
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


class AnalysisResultWrapper:
    def __init__(self, raw: dict):
        self.__raw = raw

    @property
    def progress(self) -> str:
        return self.__raw["attributes"]["status"]

    @property
    def status(self) -> StatusWrapper:
        return StatusWrapper(self.__raw["attributes"]["stats"])

    @property
    def vaccine_names(self) -> list[str]:
        return self.__raw["attributes"]["results"].keys()

    @property
    def scan_results(self) -> dict[str, VaccineResultWrapper]:
        results = {}
        raw_results = self.__raw["attributes"]["results"]

        for name in self.vaccine_names:
            result = raw_results[name]
            results[name] = VaccineResultWrapper(result)

        return results


class AnalysisCommand(Command):
    def __init__(self):
        super(AnalysisCommand, self).__init__()
        self._name = "analysis"

    def _execute(self, *args) -> CommandResult:
        if not self._has_args(1, args):
            raise InvalidArgumentException

        scan_id = args[0]
        if scan_id.lower() == "last":
            scan_id = ScanIdDB().last
            if scan_id is None:
                return CommandResult(False, "Error: There is No Scan ID.")
            scan_id = scan_id.scan_id

        client = ApiClient()
        target_endpoint = client.get_endpoint("analysis", "analysis")

        print("Fetching Data...")
        result = client.exec_endpoint(target_endpoint, path_params={"{id}": scan_id})

        if result.status_code == 403:
            return CommandResult(False, "Error: Invalid API Key.")

        result = load_json_from_str(result.text)
        result = AnalysisResultWrapper(result["data"])

        msg = f"Result: {scan_id}\n"

        if self._has_args(2, args):
            option = args[1].lower()
            if option == "verbose":
                msg += self.__do_verbose(result)
            else:
                msg += self.__do_default(result)
        else:
            msg += self.__do_default(result)

        return CommandResult(True, msg)

    def help(self) -> str:
        return "Command: analysis -> Show Your Scan Result / Usage: analysis [{SCAN_ID} | last] [verbose]"

    def __do_default(self, result: AnalysisResultWrapper) -> str:
        msg = f"Progress: {result.progress}\n"
        msg += f"Undetected: {result.status.undetected}\n"\
            + f"Harmless: {result.status.harmless}\n"\
            + f"Malicious: {result.status.malicious}\n"\
            + f"Suspicious: {result.status.suspicious}\n"\
            + f"Failure: {result.status.failure}\n"\
            + f"Timeout: {result.status.timeout}\n"\
            + f"Type Unsupported: {result.status.unsupported_type}\n"\

        return msg

    def __do_verbose(self, result: AnalysisResultWrapper) -> str:
        msg = self.__do_default(result)

        for vaccine_name in result.vaccine_names:
            vaccine_result = result.scan_results[vaccine_name]
            msg += f"\n{vaccine_result.engine_name} ({vaccine_result.engine_version}): {vaccine_result.result}"

        return msg
