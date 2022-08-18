from api.transport.http import HttpTransport
from api.controllers.http import UserExampleHttpController


class HttpClient:
    def __init__(self, transport: HttpTransport):
        """HTTP client, which provides access for all http controllers and methods.

        Args:
            transport (HttpTransport): Class providing transport to communicate with http server
        """
        self.__transport = transport

        self.users = UserExampleHttpController(self.__transport)

    @property
    def transport(self) -> HttpTransport:
        return self.__transport
