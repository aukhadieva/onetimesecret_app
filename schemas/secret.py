from pydantic import BaseModel
from typing import Optional

from pydantic.v1 import root_validator

from models.secret import Lifetime


class SecretBase(BaseModel):
    """
    Базовая модель для секретов.
    """
    secret_content: Optional[str]
    secret_password: Optional[str]
    passphrase: str
    lifetime: Lifetime

    @root_validator(pre=True)
    def check_content_or_password(cls, secret) -> dict:
        """
        Проверяет что хотя бы одно из полей секрета (secret_content или secret_password) заполнено.

        :param cls: Ссылка на SecretBase
        :param secret: Словарь, содержащий значения полей модели
        :return: secret: Обновленный словарь значений, если валидация прошла успешно
        """
        secret_content = secret.get('secret_content')
        secret_password = secret.get('secret_password')
        if not secret_content and not secret_password:
            raise ValueError('Должен быть указан либо secret_content, либо secret_password')
        return secret


class SecretCreate(SecretBase):
    """
    Модель для создания секрета.
    """
    pass


class SecretOut(BaseModel):
    """
    Модель для вывода секрета.
    """
    id: int
    link: str
