import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL'), echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
Base = declarative_base()


async def create_tables():
    """
    Подключается к базе данных и создает таблицы,
    определенные в моделях, наследующихся от класса Base.
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Создает и возвращает экземпляр сессии базы данных.
    """
    async with AsyncSessionLocal() as session:
        yield session
