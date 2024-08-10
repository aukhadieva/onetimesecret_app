from pydantic import BaseModel


class Token(BaseModel):
    """
    Модель для описания JWT токенов.
    """
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    """
    Модель для описания JWT токенов для рефреша.
    """
    refresh_token: str
