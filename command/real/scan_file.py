from api import ApiClient
from command import Command
from command.result import CommandResult
from util.json import load_json_from_str


class ScanFileCommand(Command):
    def execute(self, *args, **kwargs) -> CommandResult:
        try:
            client = ApiClient()
            target_endpoint = client.get_endpoint("files", "scan")

            file_path = ""

            if len(args) > 0 and args[0] is not None and args[0] != "":
                file_path = args[0]

            if kwargs["file_path"] is not None and kwargs["file_path"] != "":
                file_path = kwargs["file_path"]

            if file_path == "":
                raise InvalidFilePathException

            target_file = None

            try:
                target_file = open(file_path, "r")
            except FileNotFoundError:
                raise InvalidFilePathException

            if target_file is None:
                raise InvalidFilePathException

            result = client.exec_endpoint(target_endpoint, file=target_file)

            if result.status_code == 403:
                raise InvalidApiKeyException

            result = load_json_from_str(result.text)
            web_url = result["permalink"]
            resource_id = result["resource"]

            return CommandResult(True, f"Successfully Upload File.\n"
                                 + f"File Path: {file_path}\n"
                                 + f"Scan ID: {resource_id}\n"
                                 + f"Web URL: {web_url}")
        except InvalidFilePathException:
            return CommandResult(False, "Invalid File Path.")
        except InvalidApiKeyException:
            return CommandResult(False, "Invalid API Key.")


class InvalidFilePathException(Exception):
    def __init__(self):
        super().__init__()


class InvalidApiKeyException(Exception):
    def __init__(self):
        super().__init__()
