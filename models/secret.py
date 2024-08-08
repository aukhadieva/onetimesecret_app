from enum import Enum

from sqlalchemy import Column, Integer, String, CheckConstraint, Enum as EnumType, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base


class Lifetime(str, Enum):
    """
    Срок жизни секрета.
    """
    five_min = '5 минут'
    thirty_min = '30 минут'
    one_hour = '1 час'
    four_hours = '4 часа'
    twelve_hours = '12 часов'
    one_day = '1 день'
    three_days = '3 дня'
    seven_days = '7 дней'
    fourteen_days = '14 дней'


class Secret(Base):
    """
    Модель для описания секретов.
    """
    __tablename__ = 'secrets'
    id = Column(Integer, primary_key=True, index=True)
    secret_content = Column(String, nullable=True)
    secret_password = Column(String, nullable=True)
    passphrase = Column(String, nullable=False)
    lifetime = Column(EnumType(Lifetime), nullable=False)
    link = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='secrets')

    # Проверка наличия хотя бы одного из полей секрета (secret_content или secret_password)
    __table_args__ = (
        CheckConstraint(
            'secret_content IS NOT NULL OR secret_password IS NOT NULL'
        )
    )
