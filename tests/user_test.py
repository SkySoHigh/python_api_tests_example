import allure
import pytest

from api.builders.users import UserSchemaBuilder
from api.endpoints import Endpoints
from api.schemas.user_schema import UserSchemaResponse
from core.converters.users import UsersConverters


class TestUser:
    """
    This suite is for demo and its tests do not guarantee full coverage.
    The names of the tests are also for demo purposes only.
    """

    @pytest.fixture(autouse=True)
    def setup(self, db_client):
        """
        Setup_method is invoked for every test method of a class.
        """
        db_client.users.delete_all()

    @allure.issue('bug-1')
    @allure.testcase('case-1')
    def test_create_user_and_check_raw_resp(self, http_client, db_client):
        """
        This test shows how to use raw_controller, which returns only http.Response object without deserialization
        to concrete schema.
        """
        # Arrange #
        req_user_schema = UserSchemaBuilder.build_random()
        # Act #
        resp_user_schema = http_client.raw_controller.post(req_body=req_user_schema, endpoint=Endpoints.user)
        # Assert #
        assert resp_user_schema.status_code == 200
        assert resp_user_schema.content is not None  # Just check, that there is any response

    @allure.testcase('case-2')
    def test_create_user_and_check_schema_resp(self, http_client):
        # Arrange #
        req_user_schema = UserSchemaBuilder.build_random()
        # Act #
        resp_user_schema = http_client.schema_controller.post(response_schema=UserSchemaResponse,
                                                              req_body=req_user_schema,
                                                              endpoint=Endpoints.user,
                                                              )
        # Assert #
        assert resp_user_schema.state == "OK"
        assert resp_user_schema.user == req_user_schema  # UserSchema __eq__ method will be used

    @allure.testcase('case-2')
    def test_create_user_and_check_resp_schema_with_db(self, http_client, db_client):
        # Arrange #
        req_user_schema = UserSchemaBuilder.build_random()
        # Act #
        resp_user_schema = http_client.schema_controller.post(response_schema=UserSchemaResponse,
                                                              req_body=req_user_schema,
                                                              endpoint=Endpoints.user,
                                                              )
        # Assert #
        assert resp_user_schema.state == "OK" # Should be placed to HttpStates class
        assert resp_user_schema.user == req_user_schema  # UserSchema __eq__ method will be used

        db_user = db_client.users.read_by(id=resp_user_schema.user.id)
        assert len(db_user) == 1
        assert UsersConverters.entity_to_schema(db_user[0]) == resp_user_schema.user # Convert to Schema and validate with received Schema
        # Teardown
        db_client.users.delete_all()


