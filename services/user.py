from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.jwt_authorization import hash_password
from models.user import User
from schemas.user import UserCreate, UserUpdate


async def add_user(user: UserCreate, db: AsyncSession):
    """
    Добавляет нового пользователя в базу данных.

    :param user: объект, содержащий данные о новом пользователе (типа UserCreate)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: добавленный пользователь (типа UserOut)
    """
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(user_id: int, user: UserUpdate, db: AsyncSession):
    """
    Обновляет информации о пользователе.

    :param user_id: идентификатор пользователя (типа int)
    :param user: объект, содержащий данные о пользователе для обновления (типа UserUpdate)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: обновленный пользователь (типа UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    if user.password is not None and user.password != db_user.password:
        db_user.password = hash_password(user.password)

    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(user_id: int, db: AsyncSession):
    """
    Получает пользователя по идентификатору.

    :param user_id: идентификатор пользователя (типа int)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: пользователь с указанным идентификатором (типа UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user


async def get_users(db: AsyncSession):
    """
    Получает список всех пользователей.

    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: список пользователей (типа List[UserOut])
    """
    query = await db.execute(select(User))
    return query.scalars().all()


async def delete_user(user_id: int, db: AsyncSession):
    """
    Удаляет пользователя по идентификатору.

    :param user_id: идентификатор пользователя (типа int)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: удаленный пользователь (типа UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    await db.delete(db_user)
    await db.commit()
    return db_user


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
    Получает пользователя по email.

    :param email: email пользователя
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: пользователь с указанным email (типа User)
    """
    result = await db.execute(select(User).filter(User.email == email))
    db_user = result.scalars().first()
    return db_user
