import pytest
from unittest.mock import Mock
from clustaar.webhook.routing import Router
from tests.utils import FACTORY


@pytest.fixture
def handler():
    return Mock()


@pytest.fixture
def router():
    return Router()


@pytest.fixture
def http_request():
    data = {"topic": "step_reached"}
    return FACTORY.create_http_request(json=data)


@pytest.fixture
def event():
    return Mock(topic="step_reached")


class TestAdd(object):
    def test_register_a_new_route(self, router, http_request, event, handler):
        assert router.find(http_request) is None
        router.add("step_reached", handler)
        assert router.find(http_request) is not None


class TestFind(object):
    def test_returns_none_if_no_route_found(self, router, http_request):
        route = router.find(http_request)
        assert route is None

    def test_returns_right_route(self, router, handler, http_request):
        router.add("step_reached", handler)
        handler2 = Mock()
        router.add("story_fallback_triggered", handler2)

        route = router.find(http_request)
        route.process(http_request, None, None)
        assert handler.called
