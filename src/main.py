from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from src.secret import router as secret_router
from src.user import router as user_router
from src.auth import router as auth_router

from src.database import create_tables, engine

app = FastAPI()

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(user_router.router)
app.include_router(secret_router.router)
app.include_router(auth_router.router)


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
    await engine.dispose()
