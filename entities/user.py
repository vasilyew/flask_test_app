from entities.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True)
    hash_pass = Column(String(64))
    permissions = relationship('UserPermission')
