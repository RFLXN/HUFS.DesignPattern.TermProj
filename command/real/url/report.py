from api import ApiClient
from command import Command
from command.exception import InvalidArgumentException, InvalidApiKeyException
from command.result import CommandResult
from command.type.api_url import UrlReport
from db import ScanIdDB
from util.json import load_json_from_str


class ReportCommand(Command):
    def __init__(self):
        super(ReportCommand, self).__init__()
        self._name = "url-report"

    def _execute(self, *args) -> CommandResult:
        if not self._has_args(1, args):
            raise InvalidArgumentException

        url_id = args[0]

        if url_id.lower() == "last":
            url_id = ScanIdDB().last_url.object_id
            if url_id is None:
                return CommandResult(False, "There is no URL ID.")
        try:
            report = self.__fetch_report(url_id)
            if self._has_args(2, args):
                cmd = args[1]
                if cmd.lower() == "verbose":
                    return CommandResult(True, self.__create_verbose_msg(report))
                else:
                    raise InvalidArgumentException
            else:
                return CommandResult(True, self.__create_default_msg(report))
        except KeyError:
            return CommandResult(False, "Error: API Error.")

    def help(self) -> str:
        return "Command: url-report -> Show Your URL Report / Usage: url [last | {URL_ID}] [verbose]"

    def __fetch_report(self, url_id: str) -> UrlReport:
        client = ApiClient()
        target_endpoint = client.get_endpoint("url", "report")

        result = client.exec_endpoint(target_endpoint, path_params={"{id}": url_id})

        if result.status_code == 403:
            raise InvalidApiKeyException

        result = load_json_from_str(result.text)
        return UrlReport(result)

    def __create_default_msg(self, report: UrlReport) -> str:
        status = report.status
        return (f"URL: {report.url} ({report.page_title})\n"
                + f"{self.__create_catrgoty_msg(report)}\n"
                + f"Undetected: {str(status.undetected)}\n"
                + f"Harmless: {str(status.harmless)}\n"
                + f"Malicious: {str(status.malicious)}\n"
                + f"Suspicious: {str(status.suspicious)}\n"
                + f"Timeout: {str(status.timeout)}")

    def __create_catrgoty_msg(self, report: UrlReport) -> str:
        msg = "\nPage Categories\n"
        for engine_name in report.category_analyse_engine_names:
            category = report.get_category_analyse(engine_name)
            msg += f"{engine_name}: {category}\n"

        return msg

    def __create_verbose_msg(self, report: UrlReport) -> str:
        msg = self.__create_catrgoty_msg(report) + "\nScan Results\n"
        for engine_name in report.scaner_names:
            result = report.get_scan_result(engine_name)
            msg += f"{result.engine_name}: {result.result}\n"
        return msg
