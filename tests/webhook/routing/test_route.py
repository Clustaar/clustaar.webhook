import pytest
from unittest.mock import Mock
from clustaar.webhook.routing import Route
from tests.utils import FACTORY


@pytest.fixture
def handler():
    return Mock()


@pytest.fixture
def filters():
    return []


@pytest.fixture
def route(handler, filters):
    return Route("step_reached", handler, filters)


@pytest.fixture
def request():
    data = {
        "topic": "step_reached",
        "botID": "507f1f77bcf86cd799439011"
    }
    return FACTORY.create_http_request(json=data)


class TestMatches(object):
    def test_returns_true_if_route_matches_event_and_no_filters(self, route, filters, request):
        assert route.matches(request)

    def test_returns_false_if_route_does_not_match_event_name(self, filters, request):
        route = Route("story_fallback_triggered", target=None)
        assert not route.matches(request)

    def test_returns_false_if_one_filter_do_not_match(self, route, filters, request):
        filters.append(lambda request: False)
        assert not route.matches(request)

    def test_returns_true_if_all_filters_matche(self, route, filters, request):
        filters.extend([
            lambda request: True,
            lambda request: True
        ])
        assert route.matches(request)


class TestProcess(object):
    @pytest.fixture
    def response(self):
        return FACTORY.create_http_response()

    @pytest.fixture
    def event(self):
        return Mock()

    def test_forwards_call_to_handler(self, route, request, response, event, handler):
        route.process(request, response, event)
        handler.assert_called_once_with(request, response, event)
