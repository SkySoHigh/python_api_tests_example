# -*- coding: utf-8 -*-
from typing import Callable, Union

from api.controllers.base import BaseHttpController
from api.schemas.base import BaseSchema, ReqSchema, RespSchema
from configs.logger import log_func_call


class BaseSchemaController(BaseHttpController):
    """
    Contains a basic set of public methods for performing operations with http schemas.
    Each method SHOULD return Generic Schema object (RespSchema).
    """

    @log_func_call
    def post(self, response_schema: Callable[[ReqSchema], RespSchema],
             req_body: Union[BaseSchema, dict],
             query_params: Union[BaseSchema, dict] = None,
             endpoint: str = None) -> RespSchema:
        """
        Send http post request and build response object based on provided response schema
        :param response_schema: Class based on BaseSchema to be used as return object reference
        :param req_body: Instance of BaseSchema class or dict to be used as request body
        :param query_params: Instance of BaseSchema class or dict to be used as query params
        :param endpoint: Endpoint to be concatenated with base client url
        :return: Http response object
        """
        _endpoint = endpoint if endpoint else self.endpoint
        _req_body = req_body if req_body else {}
        _query_params = query_params if query_params else {}

        response = self.transport.post(url=_endpoint,
                                       json=_req_body if isinstance(_req_body, dict) else _req_body.dict(),
                                       params=_query_params if isinstance(_query_params,
                                                                          dict) else _query_params.dict(),
                                       )

        return response_schema(**response.json())
