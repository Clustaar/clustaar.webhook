from clustaar.webhook.middlewares.authenticators import StaticAuthenticator, InvalidCredentials
import pytest


@pytest.fixture
def authenticator():
    return StaticAuthenticator("admin", "p@ssword")


class TestAuthenticate(object):
    def test_raises_exception_if_invalid_username(self, authenticator):
        with pytest.raises(InvalidCredentials):
            authenticator.authenticate("gaston", "p@ssword")

    def test_raises_exception_if_invalid_password(self, authenticator):
        with pytest.raises(InvalidCredentials):
            authenticator.authenticate("admin", "wrong password")

    def test_does_not_raise_exception_if_valid_credentials(self, authenticator):
        authenticator.authenticate("admin", "p@ssword")
