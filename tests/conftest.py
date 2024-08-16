import asyncio
import uuid
from datetime import timedelta
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.auth.service import create_access_token
from src.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB_TEST, \
    ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_db, Base
from src.main import app
from src.user.models import User

DATABASE_URL_TEST = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
                     f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}')

engine_test = create_async_engine(DATABASE_URL_TEST)
AsyncSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Создает и возвращает экземпляр сессии тестовой базы данных.
    """
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True, scope='function')
async def prepare_database() -> None:
    """
    Подключается к тестовой базе данных и создает таблицы,
    определенные в моделях, наследующихся от класса Base.
    Очищает базу данных после тестов.
    :return:
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Создает и возвращает асинхронный клиент для тестирования API.
    :return:
    """
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url='http://test') as a_client:
        yield a_client


@pytest.fixture(scope='session')
def event_loop() -> AsyncGenerator[asyncio.AbstractEventLoop, None]:
    """
    Создает и возвращает новый цикл событий для тестирования.
    :return:
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def test_user() -> AsyncGenerator[User, None]:
    """
    Создает и возвращает тестового пользователя.
    :return:
    """
    unique_email = f'test_email_{uuid.uuid4()}@example.com'
    user = User(email=unique_email, password='111111')
    async with AsyncSessionLocal() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    yield user


def create_test_auth_headers_for_user(email: str) -> dict[str, str]:
    """
    Создает заголовки авторизации для пользователя по его email.

    :param email: email пользователя (тип str)
    :return: заголовки авторизации (тип dict)
    """
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES)),
    )
    return {"Authorization": f"Bearer {access_token}"}
