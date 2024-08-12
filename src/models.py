from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime,  Enum as EnumType
from sqlalchemy.orm import relationship
from enum import Enum

from src.database import Base


class Lifetime(str, Enum):
    five_min = '5 минут'
    one_hour = '1 час'
    twelve_hours = '12 часов'
    one_day = '1 день'
    seven_days = '7 дней'
    fourteen_days = '14 дней'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    secrets = relationship("Secret", back_populates='user')


class Secret(Base):
    __tablename__ = 'secrets'
    id = Column(Integer, primary_key=True, index=True)
    secret_content = Column(LargeBinary, nullable=False)
    passphrase = Column(LargeBinary, nullable=False)
    lifetime = Column(EnumType(Lifetime), nullable=False)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='secrets')
