import pytest
from clustaar.webhook.falcon import HTTPResponse


@pytest.fixture
def response():
    return HTTPResponse()


class TestJSONProperty(object):
    def test_getter_return_json_data(self, response):
        data = {"id": 1}
        response.json = data
        assert response.json == data

    def test_converts_json_to_body_string(self, response):
        response.json = {"id": 1}
        assert response.body == '{"id":1}'
