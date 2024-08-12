from celery import Celery

from src.config import CELERY_BROKER_URL, CELERY_BACKEND_URL
from tasks.tasks import burn_secret    # noqa


def make_celery():
    """
    Создает и настраивает экземпляр Celery.
    Устанавливает расписание для периодической задачи burn_secret.
    :return: экземпляр Celery
    """
    celery = Celery(
        'onetimesecret_app',
        broker=CELERY_BROKER_URL,
        backend=CELERY_BACKEND_URL
    )

    celery.autodiscover_tasks(['tasks'])
    celery.conf.beat_schedule = {
        'burn_secret': {
            'task': 'tasks.tasks.burn_secret',
            'schedule': 60.0
        }
    }

    return celery


celery = make_celery()
