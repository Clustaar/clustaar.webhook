import pytest
from tests.utils import FACTORY


@pytest.fixture
def http_request():
    return FACTORY.create_http_request(body="{}")


class TestBody(object):
    def test_returns_request_body_multiple_times(self, http_request):
        assert http_request.body == b"{}"
        assert http_request.body == b"{}"


class TestJSON(object):
    def test_returns_dict(self, http_request):
        assert http_request.json == {}
