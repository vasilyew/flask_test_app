import json
from entities.user import User


def error_response(message):
    data = {'error': message}
    return json.dumps(data)


def login_response(user_id, session, permissions):
    data = {'user_id': user_id, 'session': session, 'permissions': permissions}
    return json.dumps(data)


def user_response(user: User):
    data = {
        'id': user.id,
        'login': user.login,
        'permissions': [i.permission.name for i in user.permissions]
    }
    return data


