from pydantic import BaseModel

from models.secret import Lifetime


class SecretBase(BaseModel):
    """
    Базовая модель для секретов.
    """
    lifetime: Lifetime


class SecretCreate(SecretBase):
    """
    Модель для создания секрета.
    """
    secret_content: str


class SecretOut(BaseModel):
    """
    Модель для вывода секрета.
    """
    id: int
    passphrase: str
    link: str

    class Config:
        """
        Конфигурационный класс для настройки ORM.
        Позволяет использовать ORM-объекты для сериализации.
        """
        orm_mode = True
