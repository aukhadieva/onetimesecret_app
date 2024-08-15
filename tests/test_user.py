from httpx import AsyncClient


async def test_add_and_login_user(async_client: AsyncClient):
    """
    Тестирует создание и авторизацию нового пользователя.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return: кортеж, содержащий id созданного пользователя и заголовки авторизации с токеном доступа
    """
    response = await async_client.post('/users/', json={'email': 'test_email@example.com', 'password': '111111'})
    assert response.status_code == 201, 'Пользователь не был добавлен'
    user_id = response.json().get('id')
    token_response = await async_client.post('/login', json={'email': 'test_email@example.com',
                                                             'password': '111111'})
    assert token_response.status_code == 200, 'Не удалось получить токен'
    token = token_response.json().get('access_token')
    assert token, 'Токен не был получен'
    headers = {'Authorization': f'Bearer {token}'}
    return user_id, headers


async def test_get_users(async_client: AsyncClient):
    """
    Тестирует получение списка пользователей.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return:
    """
    user_id, headers = await test_add_and_login_user(async_client)
    response = await async_client.get('/users/', headers=headers, params={'page': 1, 'size': 50})
    assert response.status_code == 200, 'Не удалось получить список пользователей'


async def test_get_user(async_client: AsyncClient):
    """
    Тестирует получение информации о пользователе по его id.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов.
    :return:
    """
    user_id, headers = await test_add_and_login_user(async_client)
    response = await async_client.get(f'/users/{user_id}', headers=headers)
    email = response.json().get('email')
    assert response.status_code == 200, 'Не удалось найти пользователя'
    assert email == 'test_email@example.com', 'Не удалось найти пользователя'


async def test_update_user(async_client: AsyncClient):
    """
    Тестирует обновление информации о пользователе.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return:
    """
    user_id, headers = await test_add_and_login_user(async_client)
    update_data = {'email': 'updated_email@example.com', 'password': '111111'}
    response = await async_client.put(f'/users/{user_id}', headers=headers, json=update_data)
    assert response.status_code == 200, 'Не удалось обновить пользователя'


async def test_delete_user(async_client: AsyncClient):
    """
    Тестирует удаление пользователя.

    :param async_client: асинхронный клиент для выполнения HTTP-запросо
    :return:
    """
    user_id, headers = await test_add_and_login_user(async_client)
    response = await async_client.delete(f'/users/{user_id}', headers=headers)
    assert response.status_code == 200, 'Не удалось найти пользователя'
