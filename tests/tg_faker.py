import json
from urllib.parse import urlparse

from telebot.util import CustomRequestResponse


class Request:
    method: str
    token: str
    method: str

    def __init__(self, verb, url, **kwargs):
        self.verb = verb
        parsed_url = urlparse(url)
        _, token, method = parsed_url.path.split('/', 2)
        self.token = token[3:]
        self.method = method
        for k, v in kwargs.items():
            setattr(self, k, v)


class TgFaker:
    requests: list[Request]
    __mocks: dict[str, dict]

    def __init__(self):
        self.requests = []
        self.__mocks = {}

    def request_sender(self, verb, url, **kwargs):
        r = Request(verb, url, **kwargs)
        self.requests.append(r)
        response = self.__mocks.get(
            r.method, 
            dict(
                ok=False, 
                description=f"Method {r.method} doesn't mocked",
                error_code=-1,
            ),
        )
        return CustomRequestResponse(json.dumps(response))

    def response_value(self, method, result=None):
        self.__mocks[method] = dict(
            ok=True,
            result=result,
        )
