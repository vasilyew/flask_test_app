from entities.base import Base
from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    expired_date = Column(TIMESTAMP)
    user = relationship('User')
    
