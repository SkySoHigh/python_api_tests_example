# -*- coding: utf-8 -*-
from api.controllers.base import BaseHttpController
from api.schemas.user_schema import UsersSchema
from api.settings import HttpResponse
from configs.logger import log_func_call


class UsersController(BaseHttpController):
    """
    Contains specific methods for User.
    """

    @log_func_call
    def create_example(self, schema: UsersSchema) -> HttpResponse:
        # This is just an example controller with a simple method.
        # Could simply be replaced with direct call or through base controllers.

        return self.transport.post(self.endpoint, data=schema.dict())
