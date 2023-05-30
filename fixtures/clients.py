import pytest

from api.client.db import DBClient
from api.client.http import HttpClient
from api.transport.db import DbTransport
from api.transport.http import HttpTransport
from configs import ConfigProvider
from configs.logger import RequestHooks


@pytest.fixture(scope="session")
def db_client():
    transport = DbTransport(url=ConfigProvider.db.dsn, echo=ConfigProvider.db.echo_db_queries,
                            echo_pool=ConfigProvider.db.echo_connection_pool)
    db_client = DBClient(transport)
    yield db_client


@pytest.fixture(scope="session")
def http_client():
    transport = HttpTransport(base_url=ConfigProvider.http.url, headers=ConfigProvider.http.headers,
                              follow_redirects=ConfigProvider.http.follow_redirects,
                              event_hooks={'request': [RequestHooks.request_logging_hook],
                                           'response': [RequestHooks.response_logging_hook]})

    http_client = HttpClient(transport)

    yield http_client
