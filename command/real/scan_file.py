from api import ApiClient
from command import Command
from command.result import CommandResult
from util.json import load_json_from_str


class ScanFileCommand(Command):
    def execute(self, **kwargs) -> CommandResult:
        client = ApiClient()
        target_endpoint = client.get_endpoint("files", "scan")
        file_path = kwargs["file"]
        try:
            f = open(file_path, "r")
            result = client.exec_endpoint(target_endpoint, file=f)
            f.close()
            result = load_json_from_str(result.text)
            return CommandResult(True, "")
        except:
            return CommandResult(False, "")

