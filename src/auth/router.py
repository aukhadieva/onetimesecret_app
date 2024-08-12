from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import Token, RefreshToken
from src.auth.service import authenticate_user, get_user, create_refresh_token, create_access_token, validate_token
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from src.database import get_db
from src.user.models import User
from src.user.schemas import UserCreate

router = APIRouter()


@router.post('/login', response_model=Token)
async def login_for_access_token(form_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Authenticates a user and generates access and refresh tokens.

    This endpoint allows a user to log in by providing their email and password.
    If the credentials are valid, it returns an access token for authentication
    and a refresh token for obtaining new access tokens when the current one expires.

    :param form_data: The data containing the user's email and password.
    :param db: The database session dependency for user authentication.
    :return: A dictionary containing the generated access token, refresh token, and the token type (bearer).
    :raises HTTPException: If authentication fails, a 401 error will be raised
    with a message indicating incorrect credentials.
    """
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
    Refreshes the access and refresh tokens for a user.

    This endpoint accepts a refresh token and generates a new access token
    and refresh token for the user. The access token allows the user to
    access protected resources, while the refresh token can be used to
    obtain new access tokens when the current one expires.

    :param form_data: The data containing the refresh token.
    :param db: The database session dependency for accessing user data.
    :return: A dictionary containing the new access token, refresh token, and the token type (bearer).
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
