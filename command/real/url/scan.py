from api import ApiClient
from command import Command
from command.exception import InvalidArgumentException, InvalidApiKeyException
from command.result import CommandResult
from urllib.parse import quote

from db import ScanIdDB
from util.json import load_json_from_str


class ScanCommand(Command):
    def __init__(self):
        super(ScanCommand, self).__init__()
        self._name = "url-scan"

    def _execute(self, *args) -> CommandResult:
        if not self._has_args(1, args):
            raise InvalidArgumentException

        url = args[0]

        client = ApiClient()
        target_endpoint = client.get_endpoint("url", "scan")
        result = client.exec_endpoint(target_endpoint, body=f"url={quote(url)}")

        if result.status_code == 403:
            raise InvalidApiKeyException

        result = load_json_from_str(result.text)

        try:
            scan_id = result["data"]["id"]
            ScanIdDB().add_id(scan_id, url)
            return CommandResult(True, "Successfully Request URL Scan.\n"
                                 + f"URL: {url}\n"
                                 + f"Scan ID: {scan_id}")
        except KeyError:
            return CommandResult(False, "Error: API Error.")

    def help(self) -> str:
        return "Command: url-scan -> Scan URL / Usage: url-scan {URL}"
