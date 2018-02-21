from unittest.mock import Mock

import falcon
import pytest
from clustaar.webhook.middlewares import ValidateSignatureMiddleware
from tests.utils import FACTORY


@pytest.fixture
def middleware():
    return ValidateSignatureMiddleware(private_key="test")


@pytest.fixture
def response():
    return FACTORY.create_http_response()


class TestProcessRequest(object):
    def test_raises_exception_if_no_signature(self, middleware, response):
        request = FACTORY.create_http_request()
        with pytest.raises(falcon.HTTPInvalidHeader) as excinfo:
            middleware.process_resource(request, response, Mock(), {})

        exception = excinfo.value
        assert exception.description == ("The value provided for the X-Signature header is invalid. "
                                         "The request's signature is missing.")

    def test_raises_exception_if_invalid_signature(self, middleware, response):
        request = FACTORY.create_http_request(
            headers={"X-Signature": "sha1=invalid"})
        with pytest.raises(falcon.HTTPInvalidHeader) as excinfo:
            middleware.process_resource(request, response, Mock(), {})

        exception = excinfo.value
        assert exception.description == ("The value provided for the X-Signature header"
                                         " is invalid. The request's signature is invalid.")

    def test_raises_execption_if_invalid_hash_function(self, middleware, response):
        request = FACTORY.create_http_request(
            headers={"X-Signature": "md5=invalid"})
        with pytest.raises(falcon.HTTPInvalidHeader) as excinfo:
            middleware.process_resource(request, response, Mock(), {})

        exception = excinfo.value
        assert exception.description == ("The value provided for the X-Signature header is invalid. "
                                         "The request's signature hash function is "
                                         "invalid (should be one of ['sha1']).")

    def test_raises_execption_if_invalid_format(self, middleware, response):
        request = FACTORY.create_http_request(
            headers={"X-Signature": "invalid_format"})
        with pytest.raises(falcon.HTTPInvalidHeader) as excinfo:
            middleware.process_resource(request, response, Mock(), {})

        exception = excinfo.value
        assert exception.description == ("The value provided for the X-Signature header is invalid. "
                                         "The request's signature format is invalid.")

    def test_does_not_raises_exception_if_valid(self, middleware, response):
        request = FACTORY.create_http_request(body="{}",
                                              headers={"X-Signature": "sha1=7876c938d38e99b954b3d839c7bafb343d29e776"})
        middleware.process_resource(request, response, Mock(), {})
