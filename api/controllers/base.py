# -*- coding: utf-8 -*-
from api.settings import HttpTransport


class BaseHttpController:
    """
    Contains a basic set of private methods for performing operations with http objects.
    """

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def transport(self):
        return self._transport

    def __init__(self, transport: HttpTransport, endpoint: str):
        """
        Args:
            transport: HttpTransport object for executing commands via http requests (transport layer).
            endpoint: http endpoint (would be concatenated with base_url)
        """
        self._transport = transport
        self._endpoint = endpoint
