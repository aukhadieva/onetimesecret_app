import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB_TEST
from src.database import get_db, Base
from src.main import app


DATABASE_URL_TEST = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
                     f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}')

engine_test = create_async_engine(DATABASE_URL_TEST)
AsyncSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_db() -> AsyncSession:
    """
    Создает и возвращает экземпляр сессии тестовой базы данных.
    """
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
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
async def async_client() -> AsyncClient:
    """
    Создает и возвращает асинхронный клиент для тестирования API.
    :return:
    """
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url='http://test') as a_client:
        yield a_client


@pytest.fixture(scope='session')
def event_loop():
    """
    Создает и возвращает новый цикл событий для тестирования.
    :return:
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
