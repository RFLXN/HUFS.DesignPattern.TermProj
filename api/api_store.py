from os.path import dirname, realpath
from pathlib import Path
from shutil import copyfile

from structure.singleton import SingletonMeta
from util.json import load_json_from_file, write_json_to_file
from util.path_like_dict import PathLikeDict
from .api_type import ApiEndpointBuilder, EndpointParam, ApiDirectory


def _get_resource_path() -> str:
    return str((Path(dirname(realpath(__file__))) / ".." / "resource").resolve())


def _get_api_info_file_path() -> str:
    """get api-info.json files path
    :return: str
    """
    return str((Path(_get_resource_path()) / "api-info.json").resolve())


def _get_api_info() -> dict:
    """get api info
    :return: dict
    """
    return load_json_from_file(_get_api_info_file_path())


def _get_api_key_file_path() -> str:
    return str((Path(_get_resource_path()) / "api-key.json").resolve())


def _get_api_key_default_file_path() -> str:
    return str((Path(_get_resource_path()) / "api-key.default.json").resolve())


def _get_api_key() -> str:
    try:
        obj = load_json_from_file(_get_api_key_file_path())
        if obj["apiKey"] is None or obj["apiKey"] == "":
            raise Exception
        return obj["apiKey"]
    except:
        raise ApiKeyNotSetException


def _cp_default_api_key():
    copyfile(_get_api_key_default_file_path(), _get_api_key_file_path())


def _set_api_key(key: str):
    obj = {
        "apiKey": key
    }
    write_json_to_file(obj, _get_api_key_file_path())


class ApiInfoStore(metaclass=SingletonMeta):
    def __init__(self):
        self.__api_path = _get_api_info_file_path()
        self.__raw_info = _get_api_info()
        self.__api_root_url = self.__raw_info["apiRoot"]
        self.__api_directories = PathLikeDict()
        self.do_init_info()

    def do_init_info(self):
        endpoints_root_obj = self.__raw_info["endpoints"]
        directory_names = endpoints_root_obj.keys()

        for directory_name in directory_names:
            directory_obj = endpoints_root_obj[directory_name]
            directory = ApiDirectory()
            endpoint_names = directory_obj.keys()

            for endpoint_name in endpoint_names:
                endpoint_obj = directory_obj[endpoint_name]
                builder = ApiEndpointBuilder()
                builder.set_name(endpoint_name)
                builder.set_path(endpoint_obj["path"])
                builder.set_method(endpoint_obj["method"])

                try:
                    params_list = endpoint_obj["params"]
                    if params_list is not None:
                        for param_obj in params_list:
                            builder.add_param(EndpointParam(param_obj["name"], param_obj["type"]))
                except KeyError:
                    pass

                try:
                    path_params_list = endpoint_obj["pathParams"]
                    if path_params_list is not None:
                        for path_param in path_params_list:
                            builder.add_path_param(path_param)
                except KeyError:
                    pass

                directory[endpoint_name] = builder.build()
            self.__api_directories[directory_name] = directory

    @property
    def root_url(self) -> str:
        return self.__api_root_url

    def __truediv__(self, other: str) -> ApiDirectory:
        directory = self.__api_directories[other]
        if directory is None:
            raise InvalidApiDirectoryNameException
        return directory


class ApiKeyStore(metaclass=SingletonMeta):
    def __init__(self):
        self.__api_key = None

    def load_key(self) -> str:
        self.__api_key = _get_api_key()
        return self.__api_key

    def is_key_file_exist(self) -> bool:
        try:
            _get_api_key()
            return True
        except:
            return False

    def set_key(self, key: str):
        self.__api_key = key
        _set_api_key(key)

    def create_key_file(self):
        _cp_default_api_key()

    @property
    def key(self) -> str:
        if self.__api_key is None:
            raise ApiKeyNotLoadedException
        return self.__api_key


class InvalidApiDirectoryNameException(KeyError):
    def __init__(self):
        super().__init__()


class ApiKeyNotLoadedException(Exception):
    def __init__(self):
        super().__init__()


class ApiKeyNotSetException(Exception):
    def __init__(self):
        super().__init__()
