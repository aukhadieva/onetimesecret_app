from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from models.user import User
from schemas.secret import SecretOut, SecretCreate, SecretDecryptOut, SecretKeyOut
from services import secret as crud
from services.auth import get_current_user

router = APIRouter()


@router.post('/generate/', response_model=SecretKeyOut)
async def generate_secret(secret: SecretCreate, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """
    Генерирует новый секрет и сохраняет его в базе данных.

    :param secret: объект с данными о новом секрете (типа SecretCreate)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :param current_user: текущий авторизованный пользователь (типа User)
    :return: ключ секрета (типа SecretKeyOut)
    """
    return await crud.generate_secret(secret, current_user.id, db)


@router.get('/secrets/{secret_key}', response_model=SecretDecryptOut)
async def get_secret(secret_key: bytes, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """
    Получает секрет по зашифрованному ключу.

    :param secret_key: зашифрованный ключ секрета (типа bytes)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :param current_user: текущий авторизованный пользователь (типа User)
    :return: расшифрованный секрет (типа SecretDecryptOut)
    """
    return await crud.get_secret(secret_key, current_user.id, db)


@router.get('/secrets/', response_model=List[SecretOut])
async def get_secrets(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Получает список всех секретов.

    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :param current_user: текущий авторизованный пользователь (типа User)
    :return: список секретов (типа List[SecretOut])
    """
    return await crud.get_secrets(current_user.id, db)
