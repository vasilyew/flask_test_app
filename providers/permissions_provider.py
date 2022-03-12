from db import create_session
from entities.user_permission import UserPermission
from entities.permission import Permission


def set_user_permissions(user_id: int, permissions: str):
    with create_session() as session:
        session.query(UserPermission).filter(UserPermission.user_id==user_id).filter(UserPermission.permission_id!=1).delete()
        db_permissions = session.query(Permission).all()
        for db_perm in db_permissions:
            if db_perm.name in permissions:
                user_permission = UserPermission(user_id=user_id, permission_id=db_perm.id)
                session.add(user_permission)
        session.commit()
