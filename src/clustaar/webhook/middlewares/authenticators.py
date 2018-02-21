from abc import ABC, abstractmethod


class InvalidCredentials(Exception):
    """Exception raised by Authenticator when authentication failed"""


class Authenticator(ABC):
    """Authenticator interface.
    Used by authentication middlewares.
    Middleware provides credentials, authenticator validates them.
    """

    @abstractmethod
    def authenticate(self, username, password):
        """
        Validates that passed credentials are valid ones.
        If invalid it raises an InvalidCredentials exception.

        Args:
            username (str): username
            password (str): password
        """


class StaticAuthenticator(Authenticator):
    """Authenticator that validates static credentials."""

    def __init__(self, username, password):
        """
        Args:
            username (str): authenticated username
            password (str): password
        """
        self._username = username
        self._password = password

    def authenticate(self, username, password):
        """
        Validates that passed credentials are valid ones.
        If invalid it raises an InvalidCredentials exception.

        Args:
            username (str): username
            password (str): password
        """
        if username != self._username or password != self._password:
            raise InvalidCredentials()
