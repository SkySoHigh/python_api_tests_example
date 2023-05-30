import pytest


# from fixtures.clients import get_client


class Kek:

    @property
    def keksagon(self):
        return self.http_client

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, http_client):
        setattr(self, 'sobaken', 'sobaken')
        ...
