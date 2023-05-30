# -*- coding: utf-8 -*-
"""The module contains http clients."""
from api.controllers.base_raw_controller import BaseRawController
from api.controllers.base_schema_controller import BaseSchemaController
from api.controllers.users_controller import UsersController
from api.settings import HttpTransport


class HttpClient:
    def __init__(self, transport: HttpTransport):
        """HTTP client, which provides access for all http controllers and methods.

        Args:
            transport (HttpTransport): Class providing transport to communicate with http server
        """
        # Base controllers
        self.raw_controller = BaseRawController(transport, endpoint='')
        self.schema_controller = BaseSchemaController(transport, endpoint='')

        # Custom controllers
        self.users = UsersController(transport, endpoint='/users')
