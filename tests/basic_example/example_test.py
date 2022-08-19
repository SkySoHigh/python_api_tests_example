import allure
import pytest

from api.client.db import DBClient
from api.transport.db import DbTransport
from models.db.base import BaseModel
from models.db.example import ExampleTable
from models.http import ExampleModel


@allure.issue('bug-1')
@allure.testcase('case-1')
@allure.title("Creating ExampleModel object")
@allure.description("Test to show http_client usage")
def test_create_model_over_http(http_client, httpx_mock):
    # Arrange - Httpx mock #
    mock_obj = ExampleModel(title='test title', description='test desc', number=100)
    httpx_mock.add_response(status_code=200, json=mock_obj.json())

    # Act #
    test_obj = ExampleModel(title='test title', description='test desc', number=100)
    response = http_client.example.create_example(model=test_obj)

    # Assert #
    assert response.status_code == 200
    recv_obj = ExampleModel.parse_raw(response.json())
    assert test_obj == recv_obj


@pytest.fixture(scope='session')
def db_client_mock():
    transport = DbTransport(url='sqlite:///:memory:', echo=False, echo_pool=False)
    db_client = DBClient(transport)
    yield db_client


@allure.issue('bug-2')
@allure.testcase('case-2')
@allure.title("Getting object from db")
@allure.description("Test to show db_client usage")
def test_get_object_from_db(db_client_mock):
    # Arrange - Create db in memory and insert entity#
    BaseModel.metadata.create_all(bind=db_client_mock.transport.engine)
    mock_obj = ExampleTable(id=1, title='test title', description='test desc', number=100)
    db_client_mock.example.create(mock_obj)

    # Act #
    db_objs = db_client_mock.example.read_by(id=1)

    # Assert #
    assert len(db_objs) == 1
    assert db_objs[0].to_dict() == mock_obj.to_dict()
