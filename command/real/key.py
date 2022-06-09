from api import ApiClient
from api.api_store import ApiKeyNotLoadedException
from command import Command
from command.exception import InvalidArgumentException
from command.result import CommandResult


class KeyCommand(Command):
    def __init__(self):
        super(KeyCommand, self).__init__()
        self._name = "key"

    def _execute(self, *args) -> CommandResult:
        cmd = ""
        if not self._has_args(1, args):
            raise InvalidArgumentException
        cmd = args[0].lower()

        if cmd != "get" and cmd != "set":
            raise InvalidArgumentException

        if cmd == "get":
            return self.__do_get()
        elif cmd == "set":
            if not self._has_args(2, args):
                raise InvalidArgumentException
            api_key = args[1]
            return self.__do_set(api_key)

    def help(self) -> str:
        return "Command: key -> Set API Key or Get API Key / Usage: key [help | get | set {API_KEY}]"

    def __do_get(self) -> CommandResult:
        try:
            api_key = ApiClient().get_key()
            if api_key is None or api_key == "":
                raise ApiKeyNotLoadedException
            return CommandResult(True, f"API Key: {api_key}")
        except ApiKeyNotLoadedException:
            return CommandResult(False, "Error: API Key Not Set.")

    def __do_set(self, key: str) -> CommandResult:
        ApiClient().set_key(key)
        return CommandResult(True, f"API Key Set: {key}")
