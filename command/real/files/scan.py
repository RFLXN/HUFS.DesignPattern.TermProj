from api import ApiClient
from command import Command
from command.exception import InvalidApiKeyException, InvalidArgumentException
from command.result import CommandResult
from util.json import load_json_from_str


class ScanCommand(Command):
    def execute(self, *args, **kwargs) -> CommandResult:
        try:
            client = ApiClient()
            target_endpoint = client.get_endpoint("files", "scan")

            file_path = ""

            if len(args) > 1 and args[1] is not None and args[1] != "":
                file_path = args[1]

            if kwargs["file_path"] is not None and kwargs["file_path"] != "":
                file_path = kwargs["file_path"]

            if file_path == "":
                raise InvalidFilePathException

            target_file = None

            try:
                target_file = open(file_path, "rb")
            except FileNotFoundError:
                raise InvalidFilePathException
            except PermissionError:
                return CommandResult(False, "Error: Permission Denied.")

            if target_file is None:
                raise InvalidFilePathException

            result = client.exec_endpoint(target_endpoint, file=target_file)

            if result.status_code == 403:
                raise InvalidApiKeyException

            result = load_json_from_str(result.text)

            try:
                result = result["data"]
                scan_id = result["id"]
                return CommandResult(True, f"Successfully Upload File.\n"
                                     + f"File Path: {file_path}\n"
                                     + f"Scan ID: {scan_id}\n")
            except KeyError:
                return CommandResult(False, "Error: API Error.")

        except InvalidFilePathException:
            return CommandResult(False, "Error: Invalid File Path.")
        except InvalidApiKeyException:
            return CommandResult(False, "Error: Invalid API Key.")


class InvalidFilePathException(InvalidArgumentException):
    def __init__(self):
        super(InvalidFilePathException, self).__init__()
