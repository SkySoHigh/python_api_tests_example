# -*- coding: utf-8 -*-

from db.controllers.users import UsersController

from db.transport import DbTransport


class DBClient:
    def __init__(self, transport: DbTransport):
        """Database client, which provides access for all db controllers and methods.

        Args:
            transport (DbTransport): Class providing basic CRUD methods to communicate with db
        """
        self.transport = transport

        # Custom controllers #
        self.users = UsersController(self.transport)
