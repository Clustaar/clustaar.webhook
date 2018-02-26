from unittest.mock import Mock
from base64 import b64encode
import falcon
import pytest
from clustaar.webhook import Webhook
from clustaar.schemas.models import StepReachedResponse
from tests.utils import resource_content


@pytest.fixture
def webhook():
    return Webhook(private_key="test",
                   auth_username="admin",
                   auth_password="p@ssword")


@pytest.fixture
def client(webhook):
    return falcon.testing.TestClient(webhook)


@pytest.fixture
def auth_value():
    return b64encode(b"admin:p@ssword").decode()


class TestCall(object):
    def test_handles_invalid_signature(self, client, auth_value):
        result = client.simulate_post("/", headers={
            "Authorization": "Basic " + auth_value
        })
        assert result.json == {
            "description": ("The value provided for the X-Signature header is invalid. "
                            "The request's signature is missing."),
            "title": "Invalid header value"
        }

    def test_handles_invalid_credentials(self, client):
        result = client.simulate_post("/", body="{}",
                                      headers={"X-Signature": "sha1=7876c938d38e99b954b3d839c7bafb343d29e776"})
        assert result.json == {
            "description": "This call needs authentication",
            "title": "Invalid credentials"
        }

    def test_executes_handler_if_valid_request(self, webhook, client, auth_value):
        response = StepReachedResponse(actions=[], session=None)
        handler = Mock(return_value=response)
        body = resource_content("webhook_request.json")
        webhook.on("conversation.step_reached", handler)
        result = client.simulate_post(
            "/",
            body=body,
            headers={
                "X-Signature": "sha1=7b71f885ccb13d9b1e349b4e14aa28bbc3140173",
                "Authorization": "Basic " + auth_value
            }
        )
        assert handler.called


class TestOn(object):
    def test_register_a_new_event_handler(self, webhook, auth_value, client):
        response = StepReachedResponse(actions=[], session=None)
        handler = Mock(return_value=response)
        body = resource_content("webhook_request.json")
        webhook.on("conversation.step_reached", handler)
        result = client.simulate_post(
            "/",
            body=body,
            headers={
                "X-Signature": "sha1=7b71f885ccb13d9b1e349b4e14aa28bbc3140173",
                "Authorization": "Basic " + auth_value
            }
        )
        assert handler.called
