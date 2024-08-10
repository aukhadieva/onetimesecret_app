import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from schemas.auth import Token
from schemas.user import UserCreate
from services import user as crud
from services.auth import create_access_token

load_dotenv()


router = APIRouter()


@router.post('/token')
async def login(form_data: UserCreate, db: AsyncSession = Depends(get_db)) -> Token:
    """
    Аутентифицирует пользователя по email и паролю.

    :param form_data: объект, содержащий данные для аутентификации (типа UserCreate)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: JWT токен и его тип
    """
    user = await crud.get_user_by_email(form_data.email, db)
    access_token_expires = timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type='bearer')
