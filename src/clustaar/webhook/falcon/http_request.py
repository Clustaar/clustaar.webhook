from falcon import Request
import ujson as json


class HTTPRequest(Request):
    """Helper methods for falcon Request class"""
    _json = None
    _body = None

    @property
    def body(self):
        """Keeps body available for future calls

        Returns:
            str: request body
        """
        if self._body is None:
            self._body = self.stream.read()

        return self._body

    @property
    def json(self):
        """Loads JSON object from body.

        Returns:
            dict: JSON object
        """
        if self._json is None:
            self._json = json.loads(self.body)

        return self._json
