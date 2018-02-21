import pytest
from tests.utils import FACTORY


@pytest.fixture
def request():
    return FACTORY.create_http_request(body="{}")


class TestBody(object):
    def test_returns_request_body_multiple_times(self, request):
        assert request.body == b"{}"
        assert request.body == b"{}"


class TestJSON(object):
    def test_returns_dict(self, request):
        assert request.json == {}
