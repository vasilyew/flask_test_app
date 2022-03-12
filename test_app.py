from crypt import methods
from http.client import responses
from flask import Flask, render_template, request, json
from auth_decorator import access_for
from config import AppConfig, init_config
from db import init_db
from exceptions import IncorrectLoginOrPassword
from providers import user_provider
from providers import session_provider
from providers import permissions_provider
import request_schemas
from request_validation_decorator import validation_body
import responses

app = Flask(__name__)

@app.route("/")
def login_page():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
@validation_body(request_schemas.login)
def login():
    try:
        req = request.get_json()
        user_id = user_provider.chech_user_credentials(login=req['login'], password=req['password'])
        session_id = session_provider.create_user_session(user_id)
        permissions = user_provider.get_user_permissions(user_id)
        response = app.response_class(
            response=responses.login_response(user_id, session_id, permissions),
            status=200,
            mimetype='application/json'
        )
    except IncorrectLoginOrPassword as ex:
        response = app.response_class(
            response=responses.error_response(ex.txt),
            status=406,
             mimetype='application/json'
        )
    
    return response


@app.route('/users')
def users_page():
    return render_template('users.html')


@app.route("/user", methods=['GET'])
@access_for(permissions=['any'])
def get_users():
    users = user_provider.get_all_users()
    data = [responses.user_response(u) for u in users]
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/user', methods=['POST'])
@access_for(permissions=['creator'])
@validation_body(request_schemas.add_user)
def add_user():
    req = request.get_json()
    user_provider.create_user(req['login'], req['password'])
    response = app.response_class(
        status=204,
    )
    return response


@app.route('/user/<int:user_id>/permissions', methods=['PUT'])
@access_for(permissions=['editor'])
@validation_body(request_schemas.update_permissions)
def update_user(user_id):
    req = request.get_json()
    if 'admin' in req['permissions']:
        response = app.response_class(
            response=responses.error_response('Permissions "admin" is not change'),
            status=400,
            mimetype='application/json'
        )
    else:
        permissions_provider.set_user_permissions(user_id, req['permissions'])
        response = app.response_class(
            status=204,
        )
    return response


@app.route('/user/<int:user_id>', methods=['DELETE'])
@access_for(permissions=['deleter'])
def delete_user(user_id):
    user_provider.delete_user(user_id)
    response = app.response_class(
        status=204,
    )
    return response


def run():
    init_config()
    init_db()
    app.run('localhost', 5000, debug=AppConfig.debug)


run()