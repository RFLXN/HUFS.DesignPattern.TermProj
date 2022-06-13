from urllib.parse import quote

from api import ApiClient
from command import Command
from command.exception import InvalidArgumentException, InvalidApiKeyException
from command.result import CommandResult
from db import ScanIdDB
from util.json import load_json_from_str


class ScanCommand(Command):
    def __init__(self):
        super(ScanCommand, self).__init__()
        self._name = "url-scan"

    def _execute(self, *args) -> CommandResult:
        try:
            if not self._has_args(1, args):
                raise InvalidArgumentException

            url = args[0]

            print("Uploading URL...")
            scan_id = self.__send_url(url)

            print("Fetching URL ID...")
            url_id = self.__fetch_url_id(scan_id)

            ScanIdDB().add_id(scan_id, url_id, url, "URL")

            msg = ("Successfully Upload URL!\n"
                   + f"URL: {url}\n"
                   + f"Scan ID: {scan_id}\n"
                   + f"URL ID: {url_id}\n"
                   + "Type \"url-report last\" for Result.")

            return CommandResult(True, msg)

        except KeyError:
            return CommandResult(False, "Error: API Error.")

    def help(self) -> str:
        return "Command: url-scan -> Scan URL / Usage: url-scan {URL}"

    def __send_url(self, url: str) -> str:
        client = ApiClient()
        target_endpoint = client.get_endpoint("url", "scan")

        result = client.exec_endpoint(target_endpoint, body=f"url={quote(url)}")

        if result.status_code == 403:
            raise InvalidApiKeyException

        result = load_json_from_str(result.text)
        scan_id = result["data"]["id"]

        return scan_id

    def __fetch_url_id(self, scan_id: str) -> str:
        client = ApiClient()
        target_endpoint = client.get_endpoint("analysis", "analysis")

        result = client.exec_endpoint(target_endpoint, path_params={"{id}": scan_id})

        if result.status_code == 403:
            raise InvalidApiKeyException

        result = load_json_from_str(result.text)
        result = result["meta"]
        url_id = result["url_info"]["id"]

        return url_id
