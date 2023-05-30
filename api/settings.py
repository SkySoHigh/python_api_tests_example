# -*- coding: utf-8 -*-
"""The module contains http clients aliases (httpx could be simply replaced by requests)."""
from httpx import Client, Response

# aliases
HttpTransport = Client
HttpResponse = Response
