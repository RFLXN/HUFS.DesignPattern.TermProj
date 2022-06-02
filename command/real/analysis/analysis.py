from api import ApiClient
from command import Command
from command.exception import InvalidArgumentException, InvalidApiKeyException
from command.result import CommandResult
from util.json import load_json_from_str


class AnalysisCommand(Command):
    def __init__(self):
        super(AnalysisCommand, self).__init__()

    def execute(self, *args, **kwargs) -> CommandResult:
        try:
            scan_id = ""

            if len(args) >= 1 and args[0] is not None and args[0] != "":
                scan_id = args[0]

            if kwargs["scan_id"] is not None and kwargs["scan_id"] != "":
                scan_id = kwargs["scan_id"]

            if scan_id == "":
                raise InvalidScanIdException

            target_endpoint = ApiClient().get_endpoint("analysis", "analysis")

            result = ApiClient().exec_endpoint(target_endpoint, path_params={"{id}": scan_id})

            if result.status_code == 403:
                raise InvalidApiKeyException

            result = load_json_from_str(result.text)

            msg = f"RESULT: {scan_id}\n"
            try:
                result = result["data"]

                progress = result["attributes"]["status"]
                msg += f"Progress: {progress}\n"

                status = result["attributes"]["stats"]
                harmless = "Harmless: " + str(status["harmless"])
                unsupported_type = "Unsupported Type: " + str(status["type-unsupported"])
                suspicious = "Suspicious: " + str(status["suspicious"])
                timeout = "Timeout: " + str(status["timeout"])
                failure = "Failure: " + str(status["failure"])
                malicious = "Malicious: " + str(status["malicious"])
                undetected = "Undetected: " + str(status["undetected"])

                msg += f"{undetected}\n{harmless}\n{suspicious}\n{malicious}\n{unsupported_type}\n"
                msg += f"{failure}\n{timeout}\n"

                scan_result: dict = result["attributes"]["results"]
                scaner_names = scan_result.keys()
                for scaner_name in scaner_names:
                    scaner_result = scan_result[scaner_name]
                    r = scaner_result["category"]
                    engine_name = scaner_result["engine_name"]
                    engine_version = scaner_result["engine_version"]
                    t = f"{engine_name}({engine_version}): {r}"
                    msg += f"{t}\n"

            except KeyError:
                return CommandResult(False, "Error: API Error.")

            return CommandResult(True, msg)
        except InvalidScanIdException:
            return CommandResult(False, "Error: Invalid Scan ID.")
        except InvalidApiKeyException:
            return CommandResult(False, "Error: Invalid API Key.")


class InvalidScanIdException(InvalidArgumentException):
    def __init__(self):
        super(InvalidScanIdException, self).__init__()