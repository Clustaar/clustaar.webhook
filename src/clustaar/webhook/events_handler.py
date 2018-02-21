import falcon


class EventsHandler(object):
    def __init__(self, router, mapper, request_schema):
        """
        Args:
            router (Router): webhook router
            mapper (Mapper): a JSON mapper
            request_schema (Schema): schema for webhook requests
        """
        self._router = router
        self._mapper = mapper
        self._request_schema = request_schema

    def on_post(self, request, response):
        """Process incoming request.
        Find the right route and forwards the request to its handler.

        Args:
            request (HTTPRequest): incoming HTTP request
            response (HTTPResponse): outcoming HTTP response
        """
        route = self._router.find(request)
        if route:
            notification = self._mapper.load(request.json, self._request_schema)
            webhook_response = route.process(request, response, notification)
            response.json = self._mapper.dump(webhook_response)
        else:
            raise falcon.HTTPNotFound()
