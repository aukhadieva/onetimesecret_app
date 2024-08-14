from httpx import AsyncClient


async def test_add_user(async_client: AsyncClient):
    """
    Тестирует создание нового пользователя

    :param async_client: асинхронный клиент для выполнения HTTP-запросов
    :return: id созданного пользователя
    """
    response = await async_client.post('/users/', json={'email': 'test_email@example.com', 'password': '111111'})
    assert response.status_code == 201, 'Пользователь не был добавлен'
    return response.json().get('id')


async def test_login_for_access_token(async_client: AsyncClient):
    """
    Тестирует процесс входа пользователя в систему.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов.
    :return: токен доступа пользователя.
    """
    user = await test_add_user(async_client)
    token_response = await async_client.post('/login', json={'email': 'test_email@example.com', 
                                                             'password': '111111'})
    assert token_response.status_code == 200, 'Не удалось получить токен'
    token = token_response.json().get('access_token')
    assert token, 'Токен не был получен'
    return token


async def test_get_users(async_client: AsyncClient):
    """
    Тестирует получение списка пользователей.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов.
    :return: токен доступа пользователя.
    """
    token = await test_login_for_access_token(async_client)
    headers = {'Authorization': f'Bearer {token}'}
    response = await async_client.get('/users/', headers=headers, params={'page': 1, 'size': 50})
    assert response.status_code == 200, 'Не удалось получить список пользователей'


async def test_get_user(async_client: AsyncClient):
    """
    Тестирует получение информации о пользователе по его id.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов.
    :return:
    """
    user_id = await test_add_user(async_client)
    token_response = await async_client.post('/login', json={'email': 'test_email@example.com', 
                                                             'password': '111111'})
    token = token_response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = await async_client.get(f'/users/{user_id}', headers=headers)
    assert response.status_code == 200, 'Не удалось найти пользователя'


async def test_update_user(async_client: AsyncClient):
    """
    Тестирует обновление информации о пользователе.

    :param async_client: асинхронный клиент для выполнения HTTP-запросов.
    :return:
    """
    user_id = await test_add_user(async_client)
    token_response = await async_client.post('/login', json={'email': 'test_email@example.com', 
                                                             'password': '111111'})
    token = token_response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    update_data = {'email': 'updated_email@example.com', 'password': '111111'}
    response = await async_client.put(f'/users/{user_id}', headers=headers, json=update_data)
    assert response.status_code == 200, 'Не удалось обновить пользователя'


async def test_delete_user(async_client: AsyncClient):
    user_id = await test_add_user(async_client)
    token_response = await async_client.post('/login', json={'email': 'test_email@example.com',
                                                             'password': '111111'})
    token = token_response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = await async_client.delete(f'/users/{user_id}', headers=headers)
    assert response.status_code == 200, 'Не удалось найти пользователя'
