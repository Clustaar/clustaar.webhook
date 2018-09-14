import falcon
from tests.utils import FACTORY
from clustaar.webhook.middlewares.replay_prevention_middleware import ReplayPreventionMiddleware
import pytest
from freezegun import freeze_time


@pytest.fixture
def middleware():
    return ReplayPreventionMiddleware(request_max_age=5)


@pytest.fixture
def response():
    return FACTORY.create_http_response()


class TestProcessRequest(object):
    @freeze_time("Thu, 13 Sep 2018 11:48:16 GMT")
    def test_does_not_raise_error_if_young_request(self, middleware, response):
        request = FACTORY.create_http_request(headers={"Date": "Thu, 13 Sep 2018 11:48:13 GMT"})
        middleware.process_request(request, response)

    @freeze_time("Thu, 13 Sep 2018 11:48:23 GMT")
    def test_raise_error_if_old_request(self, middleware, response):
        request = FACTORY.create_http_request(headers={"Date": "Thu, 13 Sep 2018 11:48:13 GMT"})
        with pytest.raises(falcon.HTTPBadRequest):
            middleware.process_request(request, response)
