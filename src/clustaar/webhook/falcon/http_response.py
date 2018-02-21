from falcon import Response
import ujson as json


class HTTPResponse(Response):
    """Helper methods for falcon Reponse class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._json = None

    @property
    def json(self):
        """Returns json property

        Returns:
            dict
        """
        return self._json

    @json.setter
    def json(self, data):
        """Set response body with JSON data

        Args:
            data (dict): JSON data
        """
        self._json = data
        self.body = json.dumps(data)
