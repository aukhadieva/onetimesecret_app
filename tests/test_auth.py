from httpx import AsyncClient

from src.user.models import User


async def test_login_user(async_client: AsyncClient, test_user: User):
    """
    Тестирует авторизацию нового пользователя.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    """
    user_data = {'email': 'test_email@example.com', 'password': '111111'}
    response = await async_client.post('/api/users/', json=user_data)
    assert response.status_code == 201, 'Пользователь не был добавлен'
    token_response = await async_client.post('/api/auth/login', json={'email': 'test_email@example.com',
                                                                      'password': '111111'})
    assert token_response.status_code == 200, 'Не удалось получить токен'


async def test_refresh_token(async_client: AsyncClient, test_user: User):
    """
    Тестирует авторизацию пользователя с использованием refresh-токена.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    """
    user_data = {'email': 'test_email@example.com', 'password': '111111'}
    response = await async_client.post('/api/users/', json=user_data)
    assert response.status_code == 201, 'Пользователь не был добавлен'
    access_token_response = await async_client.post('/api/auth/login', json={'email': 'test_email@example.com',
                                                                             'password': '111111'})
    assert access_token_response.status_code == 200, 'Не удалось получить токен'

    token = access_token_response.json().get('access_token')
    print(token)
    refresh_token_response = await async_client.post('/api/auth/refresh_token', json={'refresh_token': token})
    assert refresh_token_response.status_code == 200, 'Не удалось получить токен'
