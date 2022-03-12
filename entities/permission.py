from entities.base import Base
from sqlalchemy import Column, Integer, String

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))