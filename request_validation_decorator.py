from functools import wraps
from flask import Response, request
from cerberus import Validator

from responses import error_response


def validation_body(schema):
    def _validation_body(f):
        @wraps(f)
        def __validation_body(*args, **kwargs):
            req = request.get_json()
            if req is None:
                return body_has_problem()
            validator = Validator(schema)
            if validator.validate(req):
                return f(*args, **kwargs)
            else:
                return body_has_problem()
        return __validation_body
    return _validation_body


def body_has_problem():
    return Response(
            response=error_response('Your request body has problem'),
            status=400,
            mimetype='application/json'
        )