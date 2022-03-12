from flask import session
from entities.session import Session
from entities.user import User
from entities.user_permission import UserPermission
from db import create_session
from exceptions import UserAlreadyExists
from exceptions import UserIsNotFound
from exceptions import IncorrectLoginOrPassword
from services.password import get_hash_password


def get_all_users():
    session = create_session()
    users = session.query(User).all()
    return users


def get_user_permissions(user_id):
    with create_session() as session:
        user = session.query(User).filter(User.id==user_id).first()
        return ';'.join([user_permission.permission.name for user_permission in user.permissions])


def create_user(login, password):
    with create_session() as session:
        user = session.query(User).filter(User.login==login).first()
        if user is not None:
            raise UserAlreadyExists()
        new_user = User(login=login, hash_pass=get_hash_password(password))
        session.add(new_user)
        session.commit()


def delete_user(user_id):
    with create_session() as session:
        session.query(Session).filter(Session.user_id==user_id).delete()
        session.query(UserPermission).filter(UserPermission.user_id==user_id).delete()
        session.query(User).filter(User.id==user_id).delete()
        session.commit()


def chech_user_credentials(login, password):
    hash_pass = get_hash_password(password)
    with create_session() as session:
        res = session.execute(
            'SELECT id FROM public.users u WHERE u.login = :login and u.hash_pass = :hash_pass',
            {'login': login, 'hash_pass': hash_pass}
        )
        for row in res:
            return row[0]
        raise IncorrectLoginOrPassword()
    