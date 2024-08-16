from httpx import AsyncClient

from src.user.models import User
from tests.conftest import create_test_auth_headers_for_user


async def test_add_user(async_client: AsyncClient):
    """
    Тестирует создание нового пользователя.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return:
    """
    user_data = {'email': 'test_email@example.com', 'password': '111111'}
    response = await async_client.post('/api/users/', json=user_data)
    data_from_response = response.json()
    assert response.status_code == 201, 'Пользователь не был добавлен'
    assert data_from_response.get('email') == user_data.get('email')


async def test_add_user_duplicate_email_error(async_client: AsyncClient):
    """
    Тестирует создание пользователя с одинаковой эл. почтой
    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return:
    """
    user_data = {'email': 'test_email@example.com', 'password': '111111'}
    user_data_same = {'email': 'test_email@example.com', 'password': '111111'}
    response = await async_client.post('/api/users/', json=user_data)
    assert response.status_code == 201, 'Пользователь не был добавлен'
    response = await async_client.post('/api/users/', json=user_data_same)
    assert response.status_code == 409, 'Нельзя добавить двух пользователей с одинаковой эл. почтой'


async def test_get_user(async_client: AsyncClient, test_user: User):
    """
    Тестирует получение пользователя по его id.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    :return:
    """
    response = await async_client.get(f'/api/users/{test_user.id}',
                                      headers=create_test_auth_headers_for_user(test_user.email))
    assert response.status_code == 200, 'Пользователь не найден'


async def test_get_users(async_client: AsyncClient, test_user: User):
    """
    Тестирует получение списка пользователей.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    :return:
    """
    response = await async_client.get('/api/users/', headers=create_test_auth_headers_for_user(test_user.email),
                                      params={'page': 1, 'size': 50})
    assert response.status_code == 200, 'Не удалось получить список пользователей'


async def test_update_user(async_client: AsyncClient, test_user: User):
    """
    Тестирует изменение пользователя.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    :return:
    """
    user_data_updated = {'email': test_user.email, 'password': '222222'}
    response = await async_client.put(f'/api/users/{test_user.id}',
                                      headers=create_test_auth_headers_for_user(test_user.email),
                                      json=user_data_updated)
    assert response.status_code == 200, 'Не удалось обновить пользователя'


async def test_delete_user(async_client: AsyncClient, test_user: User):
    """
    Тестирует удаление пользователя.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    :return:
    """
    response = await async_client.delete(f'/api/users/{test_user.id}',
                                         headers=create_test_auth_headers_for_user(test_user.email))
    assert response.status_code == 200, 'Не удалось найти пользователя'
