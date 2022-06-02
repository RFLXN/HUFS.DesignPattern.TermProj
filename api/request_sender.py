from typing import IO
from api.api_store import ApiInfoStore, ApiKeyStore
from api.api_type import ApiEndpoint
from util.http import RequestSender
from structure.singleton import SingletonMeta


class ApiRequestSender(metaclass=SingletonMeta):
    def send(self, endpoint: ApiEndpoint,
             params: dict = None,
             path_params: dict = None,
             file: IO = None):
        req = RequestSender()

        url = ApiInfoStore().root_url + endpoint.path
        if path_params is not None:
            keys = path_params.keys()
            for key in keys:
                val = path_params[key]
                url = url.replace(key, val)

        req.set_url(url) \
            .set_method(endpoint.method) \
            .add_header("x-apikey", ApiKeyStore().key) \
            .add_header("Accept", "application/json")
        if params is not None:
            for param_key in params.keys():
                param_val = params[param_key]
                req.add_param(param_key, param_val)
        if file is not None:
            req.set_file(file)

        return req.send()
