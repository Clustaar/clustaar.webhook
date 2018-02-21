from base64 import b64encode
from unittest.mock import Mock
import falcon
import pytest

from clustaar.webhook.middlewares import BasicAuthenticationMiddleware, authenticators
from tests.utils import FACTORY


@pytest.fixture
def middleware():
    authenticator = authenticators.StaticAuthenticator("admin", "p@ssword")
    return BasicAuthenticationMiddleware(authenticator)


@pytest.fixture
def response():
    return FACTORY.create_http_response()


class TestProcessRequest(object):
    def test_raises_exception_if_invalid_credentials(self, middleware, response):
        auth_value = b64encode(b"admin:invalid_password").decode()
        request = FACTORY.create_http_request(headers={"Authorization": "Basic " + auth_value})
        with pytest.raises(falcon.HTTPForbidden):
            middleware.process_resource(request, response, Mock(), {})

    def test_raises_exception_if_missing_username_or_password(self, middleware, response):
        auth_value = b64encode(b"invalid_password").decode()
        request = FACTORY.create_http_request(headers={"Authorization": "Basic " + auth_value})
        with pytest.raises(falcon.HTTPForbidden):
            middleware.process_resource(request, response, Mock(), {})

    def test_raises_exception_if_missing_auth_method(self, middleware, response):
        auth_value = b64encode(b"admin:p@ssword").decode()
        request = FACTORY.create_http_request(headers={"Authorization": auth_value})
        with pytest.raises(falcon.HTTPForbidden):
            middleware.process_resource(request, response, Mock(), {})

    def test_does_not_raise_execption_if_valid_credentials(self, middleware, response):
        auth_value = b64encode(b"admin:p@ssword").decode()
        request = FACTORY.create_http_request(headers={"Authorization": "Basic " + auth_value})
        middleware.process_resource(request, response, Mock(), {})

    def test_does_not_check_auth(self, middleware, response):
        request = FACTORY.create_http_request(body="{}")
        middleware.process_resource(request, response, Mock(basic_auth=False), {})
