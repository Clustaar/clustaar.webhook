import pytest
from clustaar.webhook.filters import JSONKeyExists
from tests.utils import FACTORY


@pytest.fixture
def filter():
    return JSONKeyExists("user.id")


class TestCall(object):
    def test_returns_false_if_key_is_absent(self, filter):
        data = {
            "user": None
        }
        request = FACTORY.create_http_request(json=data)
        assert not filter(request)

    def test_returns_true_if_key_is_present(self, filter):
        data = {
            "user": {
                "id": None
            }
        }
        request = FACTORY.create_http_request(json=data)
        assert filter(request)
