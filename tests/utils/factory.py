import urllib
import ujson
from falcon.testing.helpers import create_environ
from clustaar.webhook.falcon import HTTPResponse, HTTPRequest


class Factory(object):
    def create_http_request(self, headers=None, params=None, body=None, json=None):
        query_string = ""
        if params:
            query_string = urllib.parse.urlencode(params, True)
        if headers is None:
            headers = {}
        if json is not None:
            body = ujson.dumps(json)

        env = create_environ(headers=headers,
                             query_string=query_string,
                             body=body)
        request = HTTPRequest(env)
        return request

    def create_http_response(self):
        return HTTPResponse()
