from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import get_current_user
from src.database import get_db
from src.secret.schemas import SecretKeyOut, SecretCreate, SecretDecryptOut, SecretOut
from src.secret import service
from src.user.models import User

router = APIRouter()


@router.post('/generate/', response_model=SecretKeyOut, status_code=201, summary='Generates a new secret key.',
             description='This endpoint allows the authenticated user to create a new secret key based '
                         'on the provided secret information. '
                         'It returns the generated secret key information upon successful creation.')
async def generate_secret(secret: SecretCreate, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """
    :param secret: The data containing the details for the new secret key.
    :param db: The database session dependency for performing the secret generation.
    :param current_user: The currently authenticated user, used for associating the secret.
    :return: The generated secret key information as an instance of SecretKeyOut.
    """
    return await service.generate_secret(secret, current_user.id, db)


@router.get('/secrets/{secret_key}', response_model=SecretDecryptOut,
            summary='Retrieves and decrypts a specified secret key.',
            description='This endpoint allows the authenticated user to access and decrypt a secret associated '
                        'with the provided secret key. '
                        'It returns the decrypted secret information upon successful retrieval.')
async def get_secret(secret_key: bytes, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """
    :param secret_key: The secret key to be retrieved and decrypted.
    :param db: The database session dependency for accessing secret data.
    :param current_user: The currently authenticated user, used for permission checks.
    :return: The decrypted secret information as an instance of SecretDecryptOut.
    """
    return await service.get_secret(secret_key, current_user.id, db)
