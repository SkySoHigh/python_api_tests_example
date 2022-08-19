from api.transport.db import DbTransport
from api.controllers.db import ExampleDBController


class DBClient:
    def __init__(self, transport: DbTransport):
        """Database client, which provides access for all db controllers and methods.

        Args:
            transport (DbTransport): Class providing transport to communicate with db
        """
        self.__transport = transport

        self.example = ExampleDBController(self.__transport)

    @property
    def transport(self) -> DbTransport:
        return self.__transport
