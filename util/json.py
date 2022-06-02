import json


def load_json_from_file(path: str):
    """load json files as dict
    :param str path: json files path
    :return: dict
    """
    with open(path, mode="r", encoding="utf8") as f:
        return json.loads(f.read())


def load_json_from_str(s: str):
    """load json string to dict
    :param str s: json string
    :return: dict
    """
    return json.loads(s)


def write_json_to_file(obj, path: str):
    with open(path, mode="w") as f:
        json.dump(obj, f)