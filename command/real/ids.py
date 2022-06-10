from command import Command
from command.exception import InvalidArgumentException
from command.result import CommandResult
from db import ScanIdDB
from db.scan_id import ScanId


class IdCommand(Command):
    def __init__(self):
        super(IdCommand, self).__init__()
        self._name = "id"
        self.__db = ScanIdDB()

    def _execute(self, *args) -> CommandResult:
        if self._has_args(1, args):
            if args[0].lower() == "last":
                return self.__do_last()
            raise InvalidArgumentException
        else:
            return self.__do_list()

    def help(self) -> str:
        return "Command: id -> Get Your Scan IDs / Usage: id [last]"

    def __do_list(self) -> CommandResult:
        ids = self.__db.id_list
        if len(ids) < 1:
            return CommandResult(True, "There is no Scan ID.")
        msg = "Num / ID / Target / Date\n" + self.__make_bar(ids[0]) + "\n"

        for idx in range(len(ids)):
            id_obj = ids[idx]
            msg += self.__make_id_msg(idx, id_obj) + "\n"
        msg = msg[:-1]

        return CommandResult(True, msg)

    def __do_last(self) -> CommandResult:
        last = self.__db.last
        if last is None:
            return CommandResult(True, "There is no Scan ID.")
        return CommandResult(True, f"ID: {last.scan_id}\tTarget: {last.scan_target}\tDate: {last.date_str}")

    def __make_id_msg(self, idx: int, id_obj: ScanId) -> str:
        return f"{str(idx)}\t\t{id_obj.scan_id}\t\t{id_obj.scan_target}\t\t{id_obj.date_str}"

    def __make_bar(self, id_obj: ScanId) -> str:
        m = f"000\t\t{id_obj.scan_id}\t\t{id_obj.scan_target}\t\t{id_obj.date_str}"
        bar = ""
        for i in m:
            if i == "\t":
                bar += "==="
            else:
                bar += "="
        return bar
