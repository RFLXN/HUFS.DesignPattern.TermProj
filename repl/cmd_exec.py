from command import CommandFactory
from structure.singleton import SingletonMeta


class CommandExecutor(metaclass=SingletonMeta):
    def __init__(self):
        super(CommandExecutor, self).__init__()
        self.__cmd_fac = CommandFactory()

    def handle_command(self, cmd_name, *args):
        try:
            target_cmd = self.__cmd_fac.get_command(cmd_name)
            if target_cmd is None:
                raise KeyError
            result = target_cmd.run(*args)
            if not result.success:
                print(self.__red_text(result.result))
            else:
                print(result.result)
        except KeyError:
            print(self.__red_text("Invalid Command. Type help for Command List."))
        except:
            print((self.__red_text("An Unexpected Error Occurred.")))

    def __red_text(self, msg):
        return "\033[91m" + msg + "\033[0m"
