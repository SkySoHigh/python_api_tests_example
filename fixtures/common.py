import logging

import pytest


@pytest.fixture(scope='session')
def logger():
    logger = logging.getLogger()
    yield logger
