from command import CommandFactory
from structure.singleton import SingletonMeta


class CommandExecutor(metaclass=SingletonMeta):
    def __init__(self):
        super(CommandExecutor, self).__init__()
        self.__cmd_fac = CommandFactory()

    def handle_command(self, cmd_name, *args, **kwargs):
        try:
            target_cmd = self.__cmd_fac.get_command(cmd_name)
            if target_cmd is None:
                raise KeyError
            result = target_cmd.execute(*args, **kwargs)
            if not result.success:
                return self.__red_text(result.result)
            return result.result
        except KeyError:
            return self.__red_text("Invalid Command.")

    def __red_text(self, msg):
        return msg + "\033[91m"
