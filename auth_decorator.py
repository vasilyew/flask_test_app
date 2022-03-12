from functools import wraps
from flask import Response, request
from exceptions import SessionIsNotFound
from providers.session_provider import get_permissions

from responses import error_response


def access_for(permissions: list):
    def _access_for(f):
        @wraps(f)
        def __access_for(*args, **kwargs):
            session = request.headers.get('session')
            if session is None:
                return dont_access_response()
            try:
                user_permissions = get_permissions(session)
                print(user_permissions)
                if 'any' in permissions:
                    result = f(*args, **kwargs)
                elif 'admin' in user_permissions:
                    result = f(*args, **kwargs)
                elif len(set(user_permissions) & set(permissions)) > 0:
                    result = f(*args, **kwargs)
                else:
                    result = dont_access_response()
            except SessionIsNotFound as ex:
                result = dont_access_response()
            
            return result
        return __access_for
    return _access_for


def dont_access_response():
    return Response(
            response=error_response('You don\'t have accesss'),
            status=403,
            mimetype='application/json'
        )