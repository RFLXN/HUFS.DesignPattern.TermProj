from requests import get
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from structure.singleton import SingletonMeta


class ApiRequestSender(metaclass=SingletonMeta):
    @staticmethod
    def get(url, params, files=None):
        return get(url, files=files, params=params)

    @staticmethod
    def post(url, params, files=None):
        return get(url, files=files, params=params)