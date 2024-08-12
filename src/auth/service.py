from datetime import timedelta, datetime
from typing import Callable, Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import SECRET_JWT_KEY, JWT_ALGORITHM
from src.database import get_db
from src.user.models import User

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
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_JWT_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    except Exception:
        raise HTTPException(status_code=500, detail='Ошибка при создании токена')


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Создает JWT токен для рефреша с указанными данными и временем жизни.

    :param data: данные для токена (тип dict)
    :param expires_delta: время жизни токена в виде timedelta (тип timedelta, по умолчанию None)
    :return: JWT токен для рефреша (тип str)
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_JWT_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    except Exception:
        raise HTTPException(status_code=500, detail='Ошибка при создании токена')


def verify_password(plain_password, hashed_password) -> bool:
    """
    Верифицирует пароль с зашифрованным паролем.

    :param plain_password: пароль пользователя (тип str)
    :param hashed_password: зашифрованный пароль (тип str)
    :return: True, если пароль верен, иначе False
    """
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str, db: AsyncSession) -> User:
    """
    Получает пользователя по электронной почте.

    :param email: электронная почта пользователя (тип str)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: пользователь с указанной электронной почтой (тип User)
    """
    query = await db.execute(select(User).filter(User.email == email))
    user = query.scalars().first()
    return user


async def authenticate_user(get_user: Callable, email: str, password: str, db: AsyncSession) -> Union[User, bool]:
    """
    Аутентификация пользователя по предоставленным электронной почте и паролю.

    :param get_user: функция, которая извлекает пользователя из базы данных по предоставленной электронной почте
    :param email: электронная почта пользователя, пытающегося пройти аутентификацию (тип str)
    :param password: пароль, предоставленный пользователем для аутентификации (тип str)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: объект аутентифицированного пользователя, если аутентификация успешна, иначе False
    """
    user = await get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Получает текущего пользователя на основе предоставленного JWT токена.

    :param token: JWT токен, полученный при аутентификации (тип str)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: текущий пользователь (тип User)
    """
    exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        decoded_jwt = jwt.decode(token, SECRET_JWT_KEY, algorithms=[JWT_ALGORITHM])
        email = decoded_jwt.get('sub')
        if email is None:
            raise exception
    except jwt.PyJWTError:
        raise exception
    user = await get_user(email, db)
    if user is None:
        raise exception
    return user


async def validate_token(db: AsyncSession, token: str = Depends(oauth2_scheme)):
    """
    Валидирует JWT токен и возвращает текущего пользователя.

    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :param token: JWT токен, полученный при аутентификации (тип str)
    :return: текущий пользователь (тип User)
    """
    user = await get_current_user(db, token=token)
    return user
