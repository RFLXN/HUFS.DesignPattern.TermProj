from api import ApiClient
from api.api_store import ApiKeyNotLoadedException
from command import Command
from command.exception import InvalidArgumentException
from command.result import CommandResult


class KeyCommand(Command):
    def __init__(self):
        super(KeyCommand, self).__init__()

    def execute(self, *args, **kwargs) -> CommandResult:
        try:
            cmd = ""

            if len(args) >= 1 and args[0] is not None and args[0] != "":
                cmd = args[0]

            if kwargs["cmd"] is not None and kwargs["cmd"] != "":
                cmd = kwargs["cmd"]

            cmd = cmd.lower()

            if cmd != "help" and cmd != "get" and cmd != "set":
                raise InvalidCmdException

            if cmd == "help":
                return self.__do_help()
            elif cmd == "get":
                return self.__do_get()
            elif cmd == "set":
                api_key = ""
                if len(args) <= 2 and args[1] is not None and args[1] != "":
                    api_key = args[1]
                if kwargs["api_key"] is not None and kwargs["api_key"] != "":
                    api_key = kwargs["api_key"]
                if api_key == "":
                    raise InvalidArgumentException
                return self.__do_set(api_key)

            return CommandResult(False, "Error: An Unexpected Error Occurred.")

        except InvalidCmdException:
            return CommandResult(False, "Error: Invalid Command. Command Must be [help | get | set].")
        except InvalidArgumentException:
            return CommandResult(False, "Error: Missing API Key.")

    def __do_help(self) -> CommandResult:
        return CommandResult(True, "key [help | get].\nkey set {api_key}.")

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


class InvalidCmdException(InvalidArgumentException):
    def __init__(self):
        super(InvalidCmdException, self).__init__()
