from typing import IO

from .api_store import ApiInfoStore, ApiKeyStore
from .api_type import ApiEndpoint
from .request_sender import ApiRequestSender
from structure.singleton import SingletonMeta


class ApiClient(metaclass=SingletonMeta):
    def __init__(self):
        self.__info_store = ApiInfoStore()
        self.__key_store = ApiKeyStore()
        self.__req_sender = ApiRequestSender()
        self.__init_key()

    def set_key(self, key: str):
        if not self.__key_store.is_key_file_exist():
            self.__key_store.create_key_file()
        self.__key_store.set_key(key)

    def get_key(self):
        return self.__key_store.key

    def get_endpoint(self, dir_name: str, endpoint_name: str) -> ApiEndpoint:
        return self.__info_store / dir_name / endpoint_name

    def exec_endpoint(self, endpoint: ApiEndpoint, params: dict = None, path_params: dict = None, file: IO = None):
        return self.__req_sender.send(endpoint, params, path_params, file)

    def __init_key(self):
        if self.__key_store.is_key_file_exist():
            self.__key_store.load_key()
        else:
            self.__key_store.create_key_file()
