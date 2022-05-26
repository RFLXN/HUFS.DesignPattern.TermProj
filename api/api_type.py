from util.path_like_dict import PathLikeDict


class EndpointParam:
    def __init__(self, endpoint_name: str, endpoint_type: str):
        self.__name = endpoint_name
        self.__type = endpoint_type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> str:
        return self.__type


class ApiEndpoint:
    def __init__(self, name: str, path: str, method: str, params: list):
        self.__name = name
        self.__path = path
        self.__method = method
        self.__params = params

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self) -> str:
        return self.__path

    @property
    def method(self) -> str:
        return self.__method

    @property
    def params(self) -> list:
        return self.__params


# Builder Class for ApiEndpoint
class ApiEndpointBuilder:
    def __init__(self):
        self.__name = None
        self.__path = None
        self.__method = "GET"
        self.__params = list()

    def set_name(self, name: str):
        self.__name = name
        return self

    def set_path(self, path: str):
        self.__path = path
        return self

    def set_method(self, method: str):
        if method.upper() != "GET" and method.upper() != "POST" and method.upper() != "PUT" and method.upper() != "DELETE":
            raise InvalidHttpMethodException

        self.__method = method
        return self

    def add_params(self, param: EndpointParam):
        self.__params.append(param)
        return self

    def build(self) -> ApiEndpoint:
        if self.__name is None or self.__path is None:
            raise EmptyAttributeException

        return ApiEndpoint(self.__name, self.__path, self.__method, self.__params)


class ApiDirectory(PathLikeDict):
    def __init__(self):
        super().__init__()


class InvalidHttpMethodException(Exception):
    def __init__(self):
        super().__init__()


class EmptyAttributeException(Exception):
    def __init__(self):
        super().__init__()