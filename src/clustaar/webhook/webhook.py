import falcon
from copy import copy
from lupin import constructor
from clustaar.schemas import v1
from .falcon import HTTPResponse, HTTPRequest
from . import EventsHandler
from .middlewares import BasicAuthenticationMiddleware, ValidateSignatureMiddleware, authenticators
from .middlewares.replay_prevention_middleware import ReplayPreventionMiddleware
from .routing import Router
from .constants import REQUEST_MAX_AGE


MAPPER = v1.get_mapper(factory=constructor)


class Webhook(object):
    def __init__(
        self,
        auth_username=None,
        auth_password=None,
        private_key=None,
        middlewares=None,
        request_max_age=REQUEST_MAX_AGE,
    ):
        """
        Args:
            auth_username (str): HTTP authentication username
            auth_password (str): HTTP authentication password
            private_key (str): key used to validate signatures
            middlewares (list): list of falcon middlewares
            request_max_age (int): if request is older than this number of second it will be ignored,
                                   if None all requests are accepted
        """
        middlewares = copy(middlewares) if middlewares else []
        if private_key:
            middlewares.append(ValidateSignatureMiddleware(private_key))
        if auth_username and auth_password:
            authenticator = authenticators.StaticAuthenticator(auth_username, auth_password)
            basic_auth = BasicAuthenticationMiddleware(authenticator)
            middlewares.append(basic_auth)
        if request_max_age is not None:
            middlewares.append(ReplayPreventionMiddleware(request_max_age))

        self._api = falcon.API(
            middleware=middlewares, request_type=HTTPRequest, response_type=HTTPResponse
        )

        self._router = Router()
        events_handler = EventsHandler(self._router, MAPPER, v1.WEBHOOK_REQUEST)
        self._api.add_route("/", events_handler)

    def on(self, event, handler, filters=None):
        """Register a new handler for an event.

        Args:
            event (str): event name
            target (callable): callable for handling request
            filters (list<Filter>): route filters
        """
        self._router.add(event, handler, filters)

    def __call__(self, *args, **kwargs):
        """WSGI protocol.
        Forwards call to falcon handler.
        """
        return self._api(*args, **kwargs)
