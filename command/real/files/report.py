from api import ApiClient
from command import Command
from command.exception import InvalidApiKeyException, InvalidArgumentException
from command.result import CommandResult
from command.type.api_file import FileReport
from db import ScanIdDB
from util.json import load_json_from_str


class ReportCommand(Command):
    def __init__(self):
        super(ReportCommand, self).__init__()
        self._name = "file-report"

    def _execute(self, *args) -> CommandResult:
        if not self._has_args(1, args):
            raise InvalidArgumentException
        file_id = args[0]

        if file_id.lower() == "last":
            last_file = ScanIdDB().last_file
            if last_file is None:
                return CommandResult(True, "There is no File ID")
            file_id = last_file.object_id

        try:
            print("Fetching Report Data...")
            report = self.__fetch_report(file_id)

            if not self._has_args(2, args):
                return CommandResult(True, self.__create_default_msg(report))
            else:
                cmd = args[1]
                if cmd.lower() == "verbose":
                    return CommandResult(True, self.__create_verbose_msg(report))
                else:
                    raise InvalidArgumentException

        except KeyError:
            return CommandResult(False, "Error: API Error.")

    def help(self) -> str:
        return "Command: report -> Show Your File Report / Usage: report [last | {FILE_ID}] [verbose]"

    def __fetch_report(self, file_id: str) -> FileReport:
        client = ApiClient()
        target_endpoint = client.get_endpoint("files", "report")

        result = client.exec_endpoint(target_endpoint, path_params={"{id}": file_id})

        if result.status_code == 403:
            raise InvalidApiKeyException

        result = load_json_from_str(result.text)
        return FileReport(result)

    def __create_default_msg(self, report: FileReport) -> str:
        status = report.file_status
        return (f"File: {report.file_name} ({report.file_extension} / {report.file_type}) Size: {report.file_size}B\n"
                   + f"Undetected: {str(status.undetected)}\n"
                   + f"Harmless: {str(status.harmless)}\n"
                   + f"Malicious: {str(status.malicious)}\n"
                   + f"Suspicious: {str(status.suspicious)}\n"
                   + f"Failure: {str(status.failure)}\n"
                   + f"Timeout: {str(status.timeout)}\n"
                   + f"Type Unsupported: {str(status.type_unsupported)}")

    def __create_verbose_msg(self, report: FileReport) -> str:
        status = report.file_status
        msg = self.__create_default_msg(report) + "\n\nScan Results\n"
        for scaner_name in report.scaner_names:
            scan_result = report.get_scan_result(scaner_name)
            msg += f"{scan_result.engine_name} ({scan_result.engine_version}) : {scan_result.result}\n"
        return msg
