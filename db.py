from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import AppConfig
import entities.base
import entities.user
import entities.permission
import entities.user_permission
import entities.session
from entities.user import User
from entities.permission import Permission
from entities.user_permission import UserPermission
from services.password import get_hash_password
from dictionaries.permissions import Permissions


engine = None
session = None

def init_db():
    global engine
    global session
    engine = create_engine(AppConfig.db_connection)
    session = sessionmaker(engine)
    entities.base.Base.metadata.create_all(engine)
    seed()


def create_session():
    return session()


def seed():
    session = create_session()

    for id in Permissions:
        permission = session.query(Permission).filter(Permission.id==id).first()
        if permission is None:
            entity = Permission(id=id, name=Permissions[id])
            session.add(entity)
            session.commit()


    su = session.query(User).filter(User.login=='su').first()
    if su is None:
        su = User(login = 'su', hash_pass = get_hash_password(AppConfig.suPassword))
        session.add(su)
        session.commit()
        su = session.query(User).filter(User.login=='su').first()
        su_permission = UserPermission(user_id=su.id, permission_id=1)
        session.add(su_permission)
        session.commit()
