from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate, UserUpdate, UserOut


def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием алгоритма bcrypt.

    :param password: пароль для хеширования (тип str)
    :return: захешированный пароль (тип str)
    """
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.hash(password)


async def add_user(user: UserCreate, db: AsyncSession) -> UserOut:
    """
    Добавляет нового пользователя в базу данных.

    :param user: объект, содержащий данные о новом пользователе (тип UserCreate)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: добавленный пользователь (тип UserOut)
    """
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as error:
        await db.rollback()
        raise HTTPException(status_code=409, detail='Пользователь с таким email уже существует')


async def update_user(user_id: int, current_user_id: int, user: UserUpdate, db: AsyncSession) -> UserOut:
    """
    Обновляет информации о пользователе.

    :param current_user_id: идентификатор текущего авторизованного пользователя (тип int)
    :param user_id: идентификатор пользователя (тип int)
    :param user: объект, содержащий данные о пользователе для обновления (тип UserUpdate)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: обновленный пользователь (тип UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()
    if db_user is None or user_id != current_user_id:
        raise HTTPException(status_code=404, detail='Пользователь не найден или отсутствуют права')

    if user.password is not None and user.password != db_user.password:
        db_user.password = hash_password(user.password)

    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(user_id: int, db: AsyncSession) -> UserOut:
    """
    Получает пользователя по идентификатору.

    :param user_id: идентификатор пользователя (тип int)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: пользователь с указанным идентификатором (тип UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user


async def get_users(db: AsyncSession) -> [User]:
    """
    Получает всех пользователей.

    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: список всех пользователей (тип Sequence[User])
    """
    query = await db.execute(select(User))
    return query.scalars().all()


async def delete_user(user_id: int, current_user_id: int, db: AsyncSession) -> UserOut:
    """
    Удаляет пользователя по идентификатору.

    :param current_user_id: идентификатор текущего авторизованного пользователя (тип int)
    :param user_id: идентификатор пользователя (тип int)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: удаленный пользователь (тип UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()
    if db_user is None or user_id != current_user_id:
        raise HTTPException(status_code=404, detail='Пользователь не найден или отсутствуют права')
    await db.delete(db_user)
    await db.commit()
    return db_user
