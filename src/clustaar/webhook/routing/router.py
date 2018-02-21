from collections import defaultdict
from . import Route


class Router(object):
    """Router is responsible to route the incoming request to right
    route.
    When a route matches the request, the router forwards it to the route
    in order to process the request.
    """

    def __init__(self):
        self._routes = defaultdict(list)

    def add(self, event, target, filters=None):
        """Register a new handler for an event.

        Args:
            event (str): event name
            target (callable): callable for handling request
            filters (list<Filter>): route filters
        """
        route = Route(event, target, filters)
        self._routes[event].append(route)

    def find(self, request):
        """Returns route corresponding to request.

        Args:
            request (HTTPRequest): incoming HTTP request

        Returns:
            Route
        """
        topic = request.json.get("topic")
        routes = self._routes[topic]
        for route in routes:
            if route.matches(request):
                return route

        return None
