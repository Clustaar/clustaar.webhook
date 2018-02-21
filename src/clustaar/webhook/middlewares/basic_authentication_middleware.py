from base64 import b64decode
import falcon
from .authenticators import InvalidCredentials


class BasicAuthenticationMiddleware(object):
    """Perform a HTTP basic authentication of the request."""

    def __init__(self, authenticator):
        """
        Args:
            authenticator (Authenticator): an authenticator
        """
        self._authenticator = authenticator

    def process_resource(self, req, resp, resource, params):
        """Falcon callback.

        Args:
            req: the HTTP request
            resp: the HTTP response
        """
        if not hasattr(resource, "basic_auth") or resource.basic_auth:
            username, password = self._get_credentials(req)
            try:
                self._authenticator.authenticate(username, password)
            except InvalidCredentials:
                self._raise_invalid_credentials()

    def _get_credentials(self, request):
        """
        Returns username and password from request.

        Args:
            req: the HTTP request

        Returns:
            (username, password)
        """
        auth_header = request.get_header("Authorization") or ""
        auth_header_values = auth_header.split()
        if len(auth_header_values) != 2 or auth_header_values[0].upper() != "BASIC":
            self._raise_invalid_credentials()

        b64_credentials = auth_header_values[1]
        auth_values = b64decode(b64_credentials).decode().split(":")
        if len(auth_values) != 2:
            self._raise_invalid_credentials()

        return auth_values

    def _raise_invalid_credentials(self):
        raise falcon.HTTPForbidden(title="Invalid credentials",
                                   description="This call needs authentication")
