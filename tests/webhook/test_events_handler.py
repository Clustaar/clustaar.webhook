import pytest
import falcon
from lupin import constructor
from clustaar.schemas import v1
from clustaar.webhook import EventsHandler
from clustaar.webhook.routing import Router
from tests.utils import FACTORY


@pytest.fixture
def router():
    return Router()


@pytest.fixture
def mapper():
    return v1.get_mapper(factory=constructor)


@pytest.fixture
def handler(router, mapper):
    return EventsHandler(router, mapper, v1.WEBHOOK_REQUEST)


@pytest.fixture
def response():
    return FACTORY.create_http_response()


class TestOnPost(object):
    def test_raise_error_if_no_routes(self, handler, response):
        request = FACTORY.create_http_request(json={})
        with pytest.raises(falcon.HTTPNotFound):
            handler.on_post(request, response)
