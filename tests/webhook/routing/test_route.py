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
def http_request():
    data = {
        "topic": "step_reached",
        "botID": "507f1f77bcf86cd799439011"
    }
    return FACTORY.create_http_request(json=data)


class TestMatches(object):
    def test_returns_true_if_route_matches_event_and_no_filters(self, route, filters, http_request):
        assert route.matches(http_request)

    def test_returns_false_if_route_does_not_match_event_name(self, filters, http_request):
        route = Route("story_fallback_triggered", target=None)
        assert not route.matches(http_request)

    def test_returns_false_if_one_filter_do_not_match(self, route, filters, http_request):
        filters.append(lambda http_request: False)
        assert not route.matches(http_request)

    def test_returns_true_if_all_filters_matche(self, route, filters, http_request):
        filters.extend([
            lambda http_request: True,
            lambda http_request: True
        ])
        assert route.matches(http_request)


class TestProcess(object):
    @pytest.fixture
    def response(self):
        return FACTORY.create_http_response()

    @pytest.fixture
    def event(self):
        return Mock()

    def test_forwards_call_to_handler(self, route, http_request, response, event, handler):
        route.process(http_request, response, event)
        handler.assert_called_once_with(http_request, response, event)
