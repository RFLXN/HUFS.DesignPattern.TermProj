from command import Command
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
                if self._has_args(2, args):
                    return self.__do_last(args[1])
                else:
                    return self.__do_last("")
            else:
                return self.__do_list(args[0])
        else:
            return self.__do_list("")

    def help(self) -> str:
        return "Command: id -> Get Your Scan IDs / Usage: id [url | file] Or id last [url | file]"

    def __do_list(self, target_type: str) -> CommandResult:
        if target_type.lower() == "file" or target_type.lower() == "files":
            ids = self.__db.file_list
        elif target_type.lower() == "url" or target_type.lower() == "urls":
            ids = self.__db.url_list
        else:
            ids = self.__db.id_list

        if len(ids) < 1:
            return CommandResult(True, "There is no Scan ID.")
        msg = "Num / Target / Scan ID / Object ID / Type / Date\n" + self.__make_bar(ids[0]) + "\n"

        for idx in range(len(ids)):
            id_obj = ids[idx]
            msg += self.__make_id_msg(idx, id_obj) + "\n"
        msg = msg[:-1]

        return CommandResult(True, msg)

    def __do_last(self, target_type: str) -> CommandResult:
        if target_type.lower() == "file" or target_type.lower() == "files":
            last = self.__db.last_file
        elif target_type.lower() == "url" or target_type.lower() == "urls":
            last = self.__db.last_url
        else:
            last = self.__db.last

        if last is None:
            return CommandResult(True, "There is no Scan ID.")

        return CommandResult(True, f"Target: {last.scan_target}\n"
                             + f"Scan ID: {last.scan_id}\n"
                             + f"Object ID: {last.object_id}\n"
                             + f"Object Type: {last.target_type}\n"
                             + f"Date: {last.date_str}")

    def __make_id_msg(self, idx: int, id_obj: ScanId) -> str:
        return f"{str(idx)}\t\t" \
               + f"{id_obj.scan_target}\t\t" \
               + f"{id_obj.scan_id}\t\t" \
               + f"{id_obj.object_id}\t\t" \
               + f"{id_obj.target_type}\t\t" \
               + f"{id_obj.date_str}"

    def __make_bar(self, id_obj: ScanId) -> str:
        m = self.__make_id_msg(999, id_obj)
        bar = ""
        for i in m:
            if i == "\t":
                bar += "==="
            else:
                bar += "="
        return bar
