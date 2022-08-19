import logging

import allure


@allure.issue('bug-1')
@allure.testcase('case-1')
@allure.title("Getting main page example")
@allure.description("Description example")
def test_get_main_page(http_client):
    logging.info("Some logging from test before controller method is called")
    resp = http_client.example.get_main_page()
    logging.info("Some logging from test after controller method is called")
    assert resp.status_code == 200

