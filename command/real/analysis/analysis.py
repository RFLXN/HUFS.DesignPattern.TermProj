from api import ApiClient
from command import Command
from command.exception import InvalidArgumentException, InvalidApiKeyException
from command.result import CommandResult
from util.json import load_json_from_str, write_json_to_file
from db import ScanIdDB
from .file import FileAnalysisResultWrapper, do_file_default, do_file_verbose
from .url import UrlAnalysisResultWrapper, do_url_verbose, do_url_default


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

        meta: dict = result["meta"]
        result = result["data"]
        msg = f"Result: {scan_id}\n"
        if "file_info" in meta:
            file_id = meta["file_info"]["sha256"]
            return self.__do_file(msg, FileAnalysisResultWrapper(result), file_id, *args)
        elif "url_info" in meta:
            url_id = meta["url_info"]["id"]
            self.__do_url(msg, UrlAnalysisResultWrapper(result), url_id, *args)
        else:
            return CommandResult(False, "Error: API Error.")

    def help(self) -> str:
        return "Command: analysis -> Show Your Scan Result / Usage: analysis [{SCAN_ID} | last] [verbose]"

    def __do_file(self, base_msg: str, result: FileAnalysisResultWrapper, file_id: str, *args) -> CommandResult:
        msg = base_msg
        if self._has_args(2, args):
            option = args[1].lower()
            if option == "verbose":
                msg += do_file_verbose(result)
            else:
                msg += do_file_default(result)
        else:
            msg += do_file_default(result)

        return CommandResult(True, msg)

    def __do_url(self, base_msg: str, result: UrlAnalysisResultWrapper, url_id: str,  *args) -> CommandResult:
        msg = base_msg
        if self._has_args(2, args):
            option = args[1].lower()
            if option == "verbose":
                msg += do_url_verbose(result)
            else:
                msg += do_url_default(result)
        else:
            msg += do_url_default(result)

        # TODO: Implement do_verbose, do_default

        return CommandResult(True, msg)
