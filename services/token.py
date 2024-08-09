import os
from datetime import timedelta, datetime

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from models.user import User
from services import user as crud


load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Создает JWT токен с указанными данными и временем жизни.

    :param data: данные для токена (тип dict)
    :param expires_delta: время жизни токена в виде timedelta (тип timedelta, по умолчанию None)
    :return: JWT токен (тип str)
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_JWT_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))
        return encoded_jwt
    except Exception as error:
        raise HTTPException(status_code=500, detail='Ошибка при создании токена')


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Получает текущего пользователя на основе предоставленного JWT токена.

    :param token: JWT токен, полученный при аутентификации (тип str)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: текущий пользователь (тип User)
    """
    exception = HTTPException(
        status_code=401,
        detail='Не удалось подтвердить подлинность токена, проверьте корректность ввода или срок жизни токена',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        decoded_jwt = jwt.decode(token, os.getenv('SECRET_JWT_KEY'), algorithms=[os.getenv('JWT_ALGORITHM')])
        email = decoded_jwt.get('sub')
        if email is None:
            raise exception
    except jwt.PyJWTError:
        raise exception
    user = await crud.get_user_by_email(email, db)
    if user is None:
        raise exception
    return user
