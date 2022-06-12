from pathlib import Path
from typing import BinaryIO

from api import ApiClient
from command import Command
from command.exception import InvalidApiKeyException, InvalidArgumentException
from command.result import CommandResult
from util.json import load_json_from_str
from db import ScanIdDB


class ScanCommand(Command):
    def __init__(self):
        super(ScanCommand, self).__init__()
        self._name = "file-scan"

    def _execute(self, *args) -> CommandResult:
        try:
            if not self._has_args(1, args):
                raise InvalidArgumentException

            file_path = args[0]
            file_path = Path(file_path).resolve()

            file = self.__load_file(file_path)

            print("Uploading File...")
            scan_id = self.__upload_file(file)

            print("Fetching File ID...")
            file_id = self.__fetch_file_id(scan_id)

            ScanIdDB().add_id(scan_id, file_id, str(file_path), "File")

            msg = ("Successfully Upload File!\n"
                   + f"File Path: {str(file_path)}\n"
                   + f"Scan ID: {scan_id}\n"
                   + f"File ID: {file_id}\n"
                   + "Type \"file-report last\" for Result.")

            return CommandResult(True, msg)
        except KeyError:
            return CommandResult(False, "Error: API Error.")
        except FileNotFoundError:
            return CommandResult(False, "Error: Invalid File Path.")
        except PermissionError:
            return CommandResult(False, "Error: File Permission Denied.")

    def help(self) -> str:
        return "Command: file-scan -> Upload File and Request File Scan / Usage: file-scan {FILE_PATH}"

    def __upload_file(self, file: BinaryIO) -> str:
        client = ApiClient()
        target_endpoint = client.get_endpoint("files", "scan")

        result = client.exec_endpoint(target_endpoint, file=file)

        if result.status_code == 403:
            raise InvalidApiKeyException

        result = load_json_from_str(result.text)
        result = result["data"]
        scan_id = result["id"]

        return scan_id

    def __load_file(self, path: Path) -> BinaryIO:
        target_file = path.open("rb")
        if target_file is None:
            raise FileNotFoundError
        return target_file

    def __fetch_file_id(self, scan_id: str) -> str:
        client = ApiClient()
        target_endpoint = client.get_endpoint("analysis", "analysis")

        result = client.exec_endpoint(target_endpoint, path_params={"{id}": scan_id})

        if result.status_code == 403:
            raise InvalidApiKeyException

        result = load_json_from_str(result.text)
        result = result["meta"]
        file_id = result["file_info"]["sha256"]

        return file_id


class InvalidFilePathException(InvalidArgumentException):
    def __init__(self):
        super(InvalidFilePathException, self).__init__()
