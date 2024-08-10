from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserOut
from services import user as crud
from services.auth import get_current_user

router = APIRouter()


@router.post('/users/', response_model=UserOut)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Добавляет нового пользователя в базу данных.

    :param user: объект, содержащий данные о новом пользователе (типа UserCreate)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: добавленный пользователь (типа UserOut)
    """
    return await crud.add_user(user, db)


@router.put('/users/{user_id}', response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Обновляет данные пользователя по идентификатору.

    :param user_id: идентификатор пользователя (типа int)
    :param user: объект, содержащий данные для обновления (типа UserUpdate)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :param current_user: текущий авторизованный пользователь (типа User)
    :return: обновленный пользователь (типа UserOut)
    """
    return await crud.update_user(user_id, user, db)


@router.get('/users/{user_id}', response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Получает пользователя по идентификатору.

    :param user_id: идентификатор пользователя (типа int)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :param current_user: текущий авторизованный пользователь (типа User)
    :return: пользователь с указанным идентификатором (типа UserOut)
    """
    return await crud.get_user(user_id, db)


@router.get('/users/', response_model=List[UserOut])
async def get_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Получает список всех пользователей.

    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :param current_user: текущий авторизованный пользователь (типа User)
    :return: список пользователей (типа List[UserOut])
    """
    return await crud.get_users(db)


@router.delete('/users/{user_id}', response_model=UserOut)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Удаляет пользователя.

    :param user_id: идентификатор пользователя (типа int)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :param current_user: текущий авторизованный пользователь (типа User)
    :return: удаленный пользователь (типа UserOut)
    """
    return await crud.delete_user(user_id, db)
