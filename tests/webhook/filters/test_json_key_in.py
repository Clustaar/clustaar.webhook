import pytest
from clustaar.webhook.filters import JSONKeyIn
from tests.utils import FACTORY


@pytest.fixture
def filter():
    return JSONKeyIn("user.id", [1, 2])


class TestCall(object):
    def test_returns_false_if_value_is_absent(self, filter):
        data = {
            "user": None
        }
        request = FACTORY.create_http_request(json=data)
        assert not filter(request)

    def test_returns_false_if_value_is_invalid(self, filter):
        data = {
            "user": {
                "id": 3
            }
        }
        request = FACTORY.create_http_request(json=data)
        assert not filter(request)

    def test_returns_true_if_value_is_valid(self, filter):
        data = {
            "user": {
                "id": 1
            }
        }
        request = FACTORY.create_http_request(json=data)
        assert filter(request)
