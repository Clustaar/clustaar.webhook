import falcon
import hashlib
import hmac


SIGNATURE_HEADER = "X-Signature"


class ValidateSignatureMiddleware(object):
    """Middleware validating the request signature to
    prevent request forgery.
    If signature is invalid a HTTP 400 status code is returned.
    """

    def __init__(self, private_key):
        """
        Args:
            private_key (str): private used for validating payload signature
        """
        self._private_key = private_key.encode()
        self._hash_functions = {
            "sha1": hashlib.sha1
        }

    def process_resource(self, req, resp, resource, params):
        """Falcon callback.
        Raise error if signature is invalid.

        Args:
            req: the HTTP request
            resp: the HTTP response
        """
        signature = req.get_header(SIGNATURE_HEADER)
        if signature:
            hash_and_value = signature.split("=")
            if len(hash_and_value) != 2:
                self._raise("The request's signature format is invalid.")

            hash_function, value = hash_and_value
            self._validate_signature(req, value, hash_function)
        else:
            self._raise("The request's signature is missing.")

    def _validate_signature(self, req, signature, hash_function_name):
        """Validates that signature is correct.
        If signature is invalid it raises an HTTPInvalidHeader error.

        Args:
            req: the HTTP request
            signature (str): signature to validate
            hash_function_name (str): hash algorithm used to hash payload
        """
        hash_function = self._hash_functions.get(hash_function_name)
        if not hash_function:
            self._raise("The request's signature hash function is invalid "
                        "(should be one of %s)." % list(self._hash_functions.keys()))

        expected_signature = hmac.new(self._private_key,
                                      req.body,
                                      hash_function).hexdigest()
        if expected_signature != signature:
            self._raise("The request's signature is invalid.")

    def _raise(self, description):
        """Raises a HTTPInvalidHeader exception with descrition.

        Args:
            descrition (str): error descrition
        """
        raise falcon.HTTPInvalidHeader(description, SIGNATURE_HEADER)
