from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import get_current_user
from src.database import get_db
from src.secret.schemas import SecretKeyOut, SecretCreate, SecretDecryptOut, SecretOut
from src.secret import service
from src.user.models import User

router = APIRouter()


@router.post('/generate/', response_model=SecretKeyOut)
async def generate_secret(secret: SecretCreate, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """
    Generates a new secret key.

    This endpoint allows the authenticated user to create a new secret key
    based on the provided secret information. It returns the generated secret
    key information upon successful creation.

    :param secret: The data containing the details for the new secret key.
    :param db: The database session dependency for performing the secret generation.
    :param current_user: The currently authenticated user, used for associating the secret.
    :return: The generated secret key information as an instance of SecretKeyOut.
    """
    return await service.generate_secret(secret, current_user.id, db)


@router.get('/secrets/{secret_key}', response_model=SecretDecryptOut)
async def get_secret(secret_key: bytes, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """
    Retrieves and decrypts a specified secret key.

    This endpoint allows the authenticated user to access and decrypt a secret
    associated with the provided secret key. It returns the decrypted secret information
    upon successful retrieval.

    :param secret_key: The secret key to be retrieved and decrypted.
    :param db: The database session dependency for accessing secret data.
    :param current_user: The currently authenticated user, used for permission checks.
    :return: The decrypted secret information as an instance of SecretDecryptOut.
    """
    return await service.get_secret(secret_key, current_user.id, db)


@router.get('/secrets/', response_model=Page[SecretOut])
async def get_secrets(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves a list of all secrets associated with the authenticated user.

    This endpoint returns the secrets that belong to the currently authenticated user,
    ensuring that users can only access their own secrets.

    :param db: The database session dependency for accessing secret data.
    :param current_user: The currently authenticated user, used for filtering secrets.
    :return: A list of secret information as instances of SecretOut.
    """
    return await service.get_secrets(current_user.id, db)
