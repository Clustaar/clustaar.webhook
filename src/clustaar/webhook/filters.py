"""A filter is a way to route incoming requests to the right handler.

Basically it's just a function that returns True if the request matches
the filter condition.

Example:
    # Here is a filter that just check the present of the "X-Token" header
    def token_header_is_set(request):
        return "X-Token" in request.headers
"""
import jmespath
from .monkey_patch import patch_jmespath

KEY_NOT_FOUND = object()
patch_jmespath(key_not_found_sentinel=KEY_NOT_FOUND)


class JSONKeyEquals(object):
    """Validates that a key equals an expected value

    Example:
        data = {
            "user": {
                "id": 1
            }
        }
        filter = JSONKeyEquals("user.id", 1)

        assert filter(data)

        data["user"]["id"] = 2
        assert not filter(data)
    """

    def __init__(self, path, value):
        """
        Args:
            path (str): a valid JSON path
            value (object): expected value
        """
        self._path = jmespath.compile(path)
        self._value = value

    def __call__(self, request):
        """Validate that request JSON value is the expected one.

        Args:
            request (HTTPRequest): incoming HTTP request
        """
        return self._path.search(request.json) == self._value


class JSONKeyIn(object):
    """Validates that a key is present in a defined set of values.

    Example:
        data = {
            "user": {
                "id": 1
            }
        }
        filter = JSONKeyIn("user.id", [1, 2])

        assert filter(data)

        data["user"]["id"] = 2
        assert filter(data)

        data["user"]["id"] = 3
        assert not filter(data)
    """

    def __init__(self, path, values):
        """
        Args:
            path (str): a valid JSON path
            values (iterable): expected values
        """
        self._path = jmespath.compile(path)
        self._values = set(values)

    def __call__(self, request):
        """Validate that request JSON value is present in the expected ones.

        Args:
            request (HTTPRequest): incoming HTTP request
        """
        return self._path.search(request.json) in self._values


class JSONKeyExists(object):
    """Validates that a key is present.

    Example:
        data = {
            "user": {
                "id": 1
            }
        }
        filter = JSONKeyExists("user.id")

        assert filter(data)

        del data["user"]["id"]
        assert not filter(data)
    """

    def __init__(self, path):
        """
        Args:
            path (str): a valid JSON path
        """
        self._path = jmespath.compile(path)

    def __call__(self, request):
        """Validate that request JSON contains the key.

        Args:
            request (HTTPRequest): incoming HTTP request
        """
        return self._path.search(request.json) != KEY_NOT_FOUND


def StepID(id):
    """Validates that the data.step.id correspond to the expected id

    Args:
        id (str|list<str>): step IDs

    Returns:
        Filter
    """
    if isinstance(id, str):
        return JSONKeyEquals("data.step.id", id)
    elif isinstance(id, (list, set)):
        return JSONKeyIn("data.step.id", id)
    else:
        raise TypeError("id must be of type str or list<str>")
