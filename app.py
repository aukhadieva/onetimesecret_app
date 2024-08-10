from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.db import create_tables, AsyncSessionLocal
from routers import user, secret, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(user.router)
app.include_router(secret.router)
app.include_router(token.router)


@app.on_event('startup')
async def startup_event():
    """
    Подключается к базе данных и создает таблицы при запуске приложения.
    :return:
    """
    await create_tables()


@app.on_event('shutdown')
async def shutdown_event():
    """
    Закрывает соединение с базой данных при завершении работы приложения.
    :return:
    """
    await AsyncSessionLocal.close()
