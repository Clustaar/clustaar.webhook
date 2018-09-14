import datetime
from dateutil import parser
from dateutil.tz import tzutc
import falcon


class ReplayPreventionMiddleware(object):
    """Looks into the `Date` header of the request, if the request is older than a certain number
    of seconds then the request will be discared.
    """
    def __init__(self, request_max_age):
        """
        Args:
            request_max_age (int): maximum number of seconds a request is valid
        """
        self._request_max_age = request_max_age

    def process_request(self, req, resp):
        """Falcon callback.
        Raise error if signature is invalid.

        Args:
            req: the HTTP request
            resp: the HTTP response
        """
        date_string = req.get_header("date")
        request_date = parser.parse(date_string)
        now = datetime.datetime.now(tzutc())

        if (now.timestamp() - request_date.timestamp()) > self._request_max_age:
            raise falcon.HTTPBadRequest(description="Request is too old")
