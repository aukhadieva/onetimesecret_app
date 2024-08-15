from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from src.user import router as user_router
from src.secret import router as secret_router
from src.auth import router as auth_router


app = FastAPI()

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(user_router.router, prefix='/api', tags=['user'])
app.include_router(secret_router.router, prefix='/api', tags=['secret'])
app.include_router(auth_router.router, prefix='/api/auth', tags=['auth'])
