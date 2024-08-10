from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from models.user import User
from schemas.auth import Token, RefreshToken
from schemas.user import UserCreate
from services.auth import create_access_token, create_refresh_token, validate_token, get_user, authenticate_user
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post('/login', response_model=Token)
async def login_for_access_token(form_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Аутентифицирует пользователя по email и паролю.

    :param form_data: объект, содержащий данные для аутентификации (тип UserCreate)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: JWT токен и его тип
    """
    # user = await get_user(form_data.email, db)
    user = await authenticate_user(get_user, form_data.email, form_data.password, db)
    if not user or not isinstance(user, User):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={'sub': user.email, 'fresh': True}, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post('/refresh_token', response_model=Token)
async def refresh_token(form_data: RefreshToken, db: AsyncSession = Depends(get_db)):
    """
    Обновляет JWT токен при помощи refresh токена.

    :param form_data: объект, содержащий refresh токен (тип RefreshToken)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: новый JWT токен и его тип
    """
    user = await validate_token(db, token=form_data.refresh_token)

    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.email, "fresh": False}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
