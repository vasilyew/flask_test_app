from entities.base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class UserPermission(Base):
    __tablename__ = 'user_permissions'

    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)
    permission = relationship('Permission')