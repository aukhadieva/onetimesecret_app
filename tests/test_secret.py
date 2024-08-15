from httpx import AsyncClient

from tests.test_user import test_add_and_login_user


async def test_generate_secret(async_client: AsyncClient):
    """
    Тестирует создание нового секрета.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return: кортеж, содержащий заголовки авторизации и passphrase созданного секрета
    """
    user_id, headers = await test_add_and_login_user(async_client)
    secret_data = {'lifetime': '5 минут', 'secret_content': 'secret_content', 'passphrase': 'passphrase'}
    response = await async_client.post('/generate/', headers=headers, json=secret_data)
    assert response.status_code == 201, 'Секрет не был добавлен'
    passphrase = response.json().get('passphrase')
    return headers, passphrase


async def test_get_secret(async_client: AsyncClient):
    """
    Тестирует получение секрета по его ключу.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return:
    """
    headers, secret_key = await test_generate_secret(async_client)
    response = await async_client.get(f'/secrets/{secret_key}', headers=headers)
    assert response.status_code == 200, 'Не удалось найти секрет'


async def test_get_secrets(async_client: AsyncClient):
    """
    Тестирует получение списка секретов.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return:
    """
    user_id, headers = await test_add_and_login_user(async_client)
    response = await async_client.get('/secrets/', headers=headers, params={'page': 1, 'size': 50})
    assert response.status_code == 200, 'Не удалось получить список секретов'
