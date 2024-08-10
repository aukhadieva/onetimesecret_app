from pydantic import BaseModel


class Token(BaseModel):
    """
    Модель для описания JWT токенов.
    """
    access_token: str
    token_type: str
