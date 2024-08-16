from httpx import AsyncClient

from src.user.models import User
from tests.conftest import create_test_auth_headers_for_user


async def test_generate_secret(async_client: AsyncClient, test_user: User):
    """
    Тестирует создание нового секрета.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    :return:
    """
    secret_data = {'lifetime': '5 минут', 'secret_content': 'secret_content', 'passphrase': 'passphrase'}
    response = await async_client.post('/api/generate/', headers=create_test_auth_headers_for_user(test_user.email),
                                       json=secret_data)

    assert response.status_code == 201, 'Секрет не был добавлен'


async def test_get_secret(async_client: AsyncClient, test_user: User):
    """
    Тестирует получение секрета по его ключу.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    :return:
    """
    secret_data = {'lifetime': '5 минут', 'secret_content': 'secret_content', 'passphrase': 'passphrase'}
    response = await async_client.post('/api/generate/', headers=create_test_auth_headers_for_user(test_user.email),
                                       json=secret_data)
    secret_key = response.json().get('passphrase')
    response = await async_client.get(f'/api/secrets/{secret_key}',
                                      headers=create_test_auth_headers_for_user(test_user.email))
    assert response.status_code == 200, 'Не удалось найти секрет'


async def test_get_secrets(async_client: AsyncClient, test_user: User):
    """
    Тестирует получение списка секретов.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :param test_user: тестовый пользователь
    :return:
    """
    response = await async_client.get('/api/secrets/', headers=create_test_auth_headers_for_user(test_user.email),
                                      params={'page': 1, 'size': 50})
    assert response.status_code == 200, 'Не удалось получить список секретов'
