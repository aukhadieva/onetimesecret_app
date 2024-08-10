from enum import Enum

from sqlalchemy import Column, Integer, Enum as EnumType, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from database.db import Base


class Lifetime(str, Enum):
    """
    Срок жизни секрета.
    """
    five_min = '5 минут'
    one_hour = '1 час'
    twelve_hours = '12 часов'
    one_day = '1 день'
    seven_days = '7 дней'
    fourteen_days = '14 дней'


class Secret(Base):
    """
    Модель для описания секретов.
    """
    __tablename__ = 'secrets'
    id = Column(Integer, primary_key=True, index=True)
    secret_content = Column(LargeBinary, nullable=False)
    passphrase = Column(LargeBinary, nullable=False)
    lifetime = Column(EnumType(Lifetime), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='secrets')
