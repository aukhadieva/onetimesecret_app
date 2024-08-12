from datetime import datetime

from pydantic import BaseModel

from src.models import Lifetime


class SecretBase(BaseModel):
    """
    Базовая модель для секретов.
    """
    lifetime: Lifetime
    secret_content: bytes
    passphrase: bytes


class SecretCreate(SecretBase):
    """
    Модель для создания секрета.
    """
    pass


class SecretOut(SecretBase):
    """
    Модель для вывода секрета.
    """
    id: int
    user_id: int
    created_at: datetime

    class Config:
        """
        Конфигурационный класс для настройки ORM.
        Позволяет использовать ORM-объекты для сериализации.
        """
        orm_mode = True


class SecretDecryptOut(BaseModel):
    """
    Модель для вывода расшифрованного секрета.
    """
    secret_content: str


class SecretKeyOut(BaseModel):
    """
    Модель для вывода секретного ключа.
    """
    passphrase: bytes
