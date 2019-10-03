from freezegun import freeze_time
from unittest.mock import Mock
from base64 import b64encode
import falcon
import pytest
from clustaar.webhook import Webhook
from clustaar.schemas.models import StepReachedResponse
from tests.utils import resource_content


@pytest.fixture
def webhook():
    return Webhook(
        private_key="test", auth_username="admin", auth_password="p@ssword", request_max_age=None
    )


@pytest.fixture
def client(webhook):
    return falcon.testing.TestClient(webhook)


@pytest.fixture
def auth_value():
    return b64encode(b"admin:p@ssword").decode()


class TestCall(object):
    def test_handles_invalid_signature(self, client, auth_value):
        result = client.simulate_post("/", headers={"Authorization": "Basic " + auth_value})
        assert result.json == {
            "description": (
                "The value provided for the X-Hub-Signature header is invalid. "
                "The request's signature is missing."
            ),
            "title": "Invalid header value",
        }

    def test_handles_invalid_credentials(self, client):
        result = client.simulate_post(
            "/",
            body="{}",
            headers={"X-Hub-Signature": "sha1=fc2bdea0e6a9e0dc333dece7568b5c3337a92342"},
        )
        assert result.json == {
            "description": "This call needs authentication",
            "title": "Invalid credentials",
        }

    def test_executes_handler_if_valid_request(self, webhook, client, auth_value):
        response = StepReachedResponse(actions=[], session=None)
        handler = Mock(return_value=response)
        body = resource_content("webhook_request.json")
        webhook.on("conversation.step_reached", handler)
        client.simulate_post(
            "/",
            body=body,
            headers={
                "X-Hub-Signature": "sha1=c401ad18c5ed1b0b19d37a4e0e5dab958b6b9a2f",
                "Authorization": "Basic " + auth_value,
            },
        )
        assert handler.called

    @freeze_time("Thu, 13 Sep 2018 11:48:23 GMT")
    def test_handles_old_requests(self, client, auth_value):
        webhook = Webhook(request_max_age=5)
        client = falcon.testing.TestClient(webhook)
        body = resource_content("webhook_request.json")
        result = client.simulate_post(
            "/",
            body=body,
            headers={
                "X-Hub-Signature": "sha1=c401ad18c5ed1b0b19d37a4e0e5dab958b6b9a2f",
                "Authorization": "Basic " + auth_value,
                "Date": "Thu, 13 Sep 2018 11:48:13 GMT",
            },
        )
        assert result.json == {"description": "Request is too old", "title": "400 Bad Request"}


class TestOn(object):
    def test_register_a_new_event_handler(self, webhook, auth_value, client):
        response = StepReachedResponse(actions=[], session=None)
        handler = Mock(return_value=response)
        body = resource_content("webhook_request.json")
        webhook.on("conversation.step_reached", handler)
        client.simulate_post(
            "/",
            body=body,
            headers={
                "X-Hub-Signature": "sha1=c401ad18c5ed1b0b19d37a4e0e5dab958b6b9a2f",
                "Authorization": "Basic " + auth_value,
            },
        )
        assert handler.called
