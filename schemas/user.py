from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """
    Базовая модель для описания пользователей.
    """
    email: EmailStr
    password: str


class UserCreate(UserBase):
    """
    Модель создания пользователя с полями email и password.
    """
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserUpdate(UserBase):
    """
    Модель для изменения пользователей с полями email и password.
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserOut(UserBase):
    """
    Модель для вывода пользователей с полями id, email и password.
    """
    id: int
