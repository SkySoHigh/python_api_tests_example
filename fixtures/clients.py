import pytest

from api.client.db import DBClient
from api.client.http import HttpClient
from api.transport.db import DbTransport
from api.transport.http import HttpTransport
from configs import DbConfig, HttpConfig
from libs.logger import RequestHooks


@pytest.fixture(scope="session")
def db_client():
    transport = DbTransport(url=DbConfig.DSN, echo=DbConfig.ECHO_DB_QUERIES, echo_pool=DbConfig.ECHO_CONNECTION_POOL)
    db_client = DBClient(transport)
    yield db_client


@pytest.fixture(scope="session")
def http_client():
    transport = HttpTransport(base_url=HttpConfig.URL, headers=HttpConfig.DEFAULT_HEADERS,
                              follow_redirects=HttpConfig.FOLLOW_REDIRECTS,
                              event_hooks={'request': [RequestHooks.request_logging_hook],
                                           'response': [RequestHooks.response_logging_hook]})

    http_client = HttpClient(transport)

    yield http_client
