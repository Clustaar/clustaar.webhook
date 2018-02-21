class Route(object):
    """A route is responsible of telling the router if it can handler a request.
    If route matches a request router ask route to process the request.
    """

    def __init__(self, event, target, filters=None):
        """
        Args:
            event (str): event name
            target (callable): callable for handling request
            filters (list<Filter>): if provided this route will match only if all filters match
        """
        self._event = event
        self._target = target
        self._filters = filters if filters is not None else ()

    def matches(self, request):
        """Returns if route can handle the incoming request

        Args:
            request (HTTPRequest): incoming HTTP request

        Returns:
            bool: True if route matches request
        """
        if request.json["topic"] != self._event:
            return False

        for filter in self._filters:
            if not filter(request):
                return False

        return True

    def process(self, request, response, notification):
        """Forwards request to handler in order to process it.

        Args:
            request (HTTPRequest): incoming HTTP request
            response (HTTPResponse): outcoming HTTP response
            webhook_request (WebhookRequest): incoming webhook notification
        """
        return self._target(request, response, notification)
