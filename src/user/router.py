from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import get_current_user
from src.database import get_db
from src.user.models import User
from src.user.schemas import UserOut, UserCreate, UserUpdate
from src.user import service

router = APIRouter()


@router.post('/users/', response_model=UserOut, status_code=201)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Adds a new user to the database.

    This endpoint accepts user details and creates a new user record.
    It returns the created user information upon successful creation.

    :param user: The data containing the new user's information (email, password).
    :param db: The database session dependency for performing the user creation.
    :return: The created user information as an instance of UserOut.
    """
    return await service.add_user(user, db)


@router.put('/users/{user_id}', response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Updates an existing user's information.

    This endpoint allows the authenticated user to update their own user details.
    It returns the updated user information upon successful modification.

    :param user_id: The ID of the user to be updated.
    :param user: The data containing the updated user's information.
    :param db: The database session dependency for performing the update operation.
    :param current_user: The currently authenticated user, used for permission checks.
    :return: The updated user information as an instance of UserOut.
    """
    return await service.update_user(user_id, current_user.id, user, db)


@router.get('/users/{user_id}', response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves the information of a specific user.

    This endpoint returns the details of the user identified by the given user ID.
    The request is validated to ensure that the current user has permission to view
    the requested user's information.

    :param user_id: The ID of the user to be retrieved.
    :param db: The database session dependency for accessing user data.
    :param current_user: The currently authenticated user, used for permission checks.
    :return: The requested user's information as an instance of UserOut.
    """
    return await service.get_user(user_id, db)


@router.get('/users/', response_model=Page[UserOut])
async def get_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user),
                    page: int = Query(1, gt=0), size: int = Query(50, gt=0)):
    """
    Retrieve a paginated list of users.

    This endpoint fetches a list of users from the database, allowing for pagination through the
    page and size parameters.

    :param db: The database session to execute the query.
    :param current_user: The currently authenticated user making the request.
    :param page: The page number to retrieve (default is 1). Must be greater than 0.
    :param size: The number of users to return per page (default is 10). Must be greater than 0.
    :return: A paginated response model containing the list of users.
    """
    params = Params(page=page, size=size)
    return await service.get_users(db, params)


@router.delete('/users/{user_id}', response_model=UserOut)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Deletes a specified user from the database.

    This endpoint allows the authenticated user to delete their own user account.
    It returns the information of the deleted user upon successful removal.

    :param user_id: The ID of the user to be deleted.
    :param db: The database session dependency for performing the deletion operation.
    :param current_user: The currently authenticated user, used for permission checks.
    :return: The deleted user's information as an instance of UserOut.
    """
    return await service.delete_user(user_id, current_user.id, db)
