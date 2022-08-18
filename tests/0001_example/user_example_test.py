import pytest
import allure


@allure.issue('https://youtrack.ru/issue/EXAMPLE-1')
def test_users_example(db_client, http_client):
    # with db_client.transport.session_manager() as ses:
    #     users = (ses.execute('select * from users'))
    #     for user in users:
    #         print(user)
    with allure.step('Getting main page'):
        with http_client.transport as client:
            print(client.get('/').text)
