# -*- coding: utf-8 -*-
from typing import TypeVar, Generic

from api.transport.http import HttpTransport
from libs.generic_types_helpers import get_generic_type_arg

HTTP_MODEL_TYPE = TypeVar("HTTP_MODEL_TYPE")


class BaseHttpController(Generic[HTTP_MODEL_TYPE]):
    """
    Contains a basic set of private methods for performing operations with http objects.
    """

    def __init__(self, transport: HttpTransport, endpoint: str):
        """
        Args:
            transport: HttpTransport object for executing commands in the database (transport layer).
            endpoint: http endpoint (to be added to base_url)
        """
        self.model = get_generic_type_arg(self)[0]
        self.transport = transport
        self.endpoint = endpoint
