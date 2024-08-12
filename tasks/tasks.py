import asyncio
from datetime import datetime

from celery import shared_task
from dateutil.relativedelta import relativedelta
from sqlalchemy import select

from src.database import AsyncSessionLocal
from src.models import Secret


async def burn_secret_async():
    """
    Удаляет из базы данных секреты, срок жизни которых истек.
    """
    async with AsyncSessionLocal() as session:
        current_datetime = datetime.utcnow()

        burn_time_5_minutes = current_datetime - relativedelta(minutes=5)
        burn_time_1_hour = current_datetime - relativedelta(hours=1)
        burn_twelve_hours = current_datetime - relativedelta(hours=12)
        burn_one_day = current_datetime - relativedelta(days=1)
        burn_seven_days = current_datetime - relativedelta(days=7)
        burn_fourteen_days = current_datetime - relativedelta(days=14)

        query = await session.execute(select(Secret).where(
            (Secret.lifetime == '5 минут') & (Secret.created_at <= burn_time_5_minutes) |
            (Secret.lifetime == '1 час') & (Secret.created_at <= burn_time_1_hour) |
            (Secret.lifetime == '12 часов') & (Secret.created_at <= burn_twelve_hours) |
            (Secret.lifetime == '1 день') & (Secret.created_at <= burn_one_day) |
            (Secret.lifetime == '7 дней') & (Secret.created_at <= burn_seven_days) |
            (Secret.lifetime == '14 дней') & (Secret.created_at <= burn_fourteen_days)
        ))

        secrets_to_delete = query.scalars().all()
        for secret in secrets_to_delete:
            await session.delete(secret)
        await session.commit()


@shared_task
def burn_secret():
    """
    Периодическая задача Celery для запуска асинхронной функции burn_secret_async
    для удаления секретов из базы данных.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(burn_secret_async())
