import os

from dotenv import load_dotenv

load_dotenv()


# Database
DATABASE_URL = os.getenv('DATABASE_URL')


# Security
SECRET_JWT_KEY = os.getenv('SECRET_JWT_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')

# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL')
