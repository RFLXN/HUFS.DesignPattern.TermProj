from typing import IO

import os
import sys

from api.api_store import ApiInfoStore, ApiKeyStore
from api.api_type import ApiEndpoint
from util.http import RequestSender

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from structure.singleton import SingletonMeta


class ApiRequestSender(metaclass=SingletonMeta):
    def send(self, endpoint: ApiEndpoint, params: dict = None, file: IO = None):
        req = RequestSender()
        req.set_url(ApiInfoStore().root_url + endpoint.path) \
            .set_method(endpoint.method) \
            .add_param("apiKey", ApiKeyStore().key)
        if params is not None:
            for param_key in params.keys():
                if param_key != "apiKey":
                    param_val = params[param_key]
                    req.add_param(param_key, param_val)
        if file is not None:
            req.set_file(file)
        return req.send()
