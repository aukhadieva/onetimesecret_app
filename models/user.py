from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base


class User(Base):
    """
    Модель для описания пользователей.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    secrets = relationship('Secret', back_populates='user')
