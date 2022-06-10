from enum import Enum

from requests import request, Response
from typing import IO


class HttpRequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class RequestSender:
    def __init__(self):
        self.__url = ""
        self.__method = HttpRequestMethod.GET
        self.__file = None
        self.__params = dict()
        self.__header = dict()
        self.__body = None

    def set_url(self, url: str):
        self.__url = url
        return self

    def set_method(self, method: HttpRequestMethod):
        self.__method = method
        return self

    def set_file(self, file: IO):
        self.__file = {"file": file}
        return self

    def add_param(self, key: str, val: str):
        self.__params[key] = val
        return self

    def add_header(self, key: str, val: str):
        self.__header[key] = val
        return self

    def set_body(self, body: str):
        self.__body = body

    def send(self) -> Response:
        if self.__url == "":
            raise InvalidRequestAttributeException
        return request(self.__method,
                       self.__url,
                       params=self.__params,
                       files=self.__file,
                       headers=self.__header,
                       data=self.__body)


class InvalidRequestAttributeException(Exception):
    def __init__(self):
        super().__init__()
