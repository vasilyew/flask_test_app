from config import AppConfig
from db import create_session
from entities.session import Session
from datetime import datetime, timedelta
import uuid

from exceptions import SessionIsNotFound


def create_user_session(user_id):
    with create_session() as session:
        expired_date = datetime.now() + timedelta(minutes=AppConfig.sessionLifetime)
        user_session = Session(user_id=user_id, id=uuid.uuid4(), expired_date=expired_date)
        session.add(user_session)
        session.commit()
        return str(user_session.id)


def get_permissions(session_id):
    with create_session() as session:
        user_session = session.query(Session).filter(Session.id==session_id).filter(Session.expired_date>datetime.now()).first()
        if user_session is None:
            raise SessionIsNotFound()
        return [user_permission.permission.name for user_permission in user_session.user.permissions]