from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import get_current_user
from src.database import get_db
from src.secret.schemas import SecretKeyOut, SecretCreate, SecretDecryptOut, SecretOut
from src.secret import service
from src.user.models import User

router = APIRouter()


@router.post('/generate/', response_model=SecretKeyOut, status_code=201)
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
async def get_secrets(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user),
                      page: int = Query(1, gt=0), size: int = Query(50, gt=0)):
    """
    Retrieve a paginated list of secrets for the current user.

    This endpoint allows the current user to access their secrets, with pagination
    support to limit the number of results returned.

    :param db: The database session to use for retrieving secrets. This is provided automatically
    by a dependency injection system.
    :param current_user: The user requesting the secrets. This is obtained from the authentication context.
    :param page: The page number to retrieve. Defaults to 1. Should be greater than 0.
    :param size: The number of secrets to return per page. Defaults to 10. Should be greater than 0.
    :return: A paginated response containing the secrets for the user, formatted according to the SecretOut model.
    """
    params = Params(page=page, size=size)
    return await service.get_secrets(current_user.id, db, params)
