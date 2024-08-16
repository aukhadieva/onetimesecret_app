# onetimesecret_app

<!-- ABOUT THE PROJECT -->
## О проекте
Проект представляет собой HTTP сервис для одноразовых секретов.
<br>
Сервис позволяет создать секрет, задать кодовую фразу для его открытия и cгенерировать код, по которому можно прочитать секрет только один раз.
<br>
- Реализованы модели (User, Secret).
- Настроена валидация и сериализация отдельно для каждого эндпоинта.
- В проекте используется JWT-авторизация, каждый эндпоинт закрыт авторизацией.
- Реализованы права доступа для объектов:
  - каждый пользователь имеет доступ только к своим секретам.
- Реализована пагинация для вывода списка пользователей и секретов (библиотека fastapi_pagination).
- Написаны тесты для проверки всех имеющихся эндпоинтов в проекте (покрытие - 84%).
- Реализована периодическая задача Celery *burn_secret* с использованием celery-beat для удаления секретов, срок жизни которых истек.
- Подключена возможность администрировать и мониторить задачи Celery через интерактивную панель Flower.
- Настроен CORS.
- Описаны Dockerfile и docker-compose.yaml. Для сервисов fastapi, postgresql, redis, celery созданы отдельные контейнеры.
- Код соответствует PEP, используется type hints.
- К публичным методам документация написана на английском языке.



**Стек:**
- FastAPI
- SQLAlchemy
- Pydantic
- Asyncpg
- Alembic
- Pyjwt
- Celery
- Redis
- PostgreSQL
- Pytest-asyncio
- Docker
- ReDoc
- Swagger


<!-- GETTING STARTED -->
## Подготовка к работе

Для запуска локальной копии выполните следующие шаги:

### Установка

1. Клонируйте проект
   ```sh
   git@github.com:aukhadieva/onetimesecret_app.git
   ```
2. Создайте в корне проекта файл .env и заполните переменные среды в соответствии с желаемой конфигурацией, используя файл .env_sample. 


### Запуск приложения
1. Для сборки образа и запуска контейнера, выполните команду
   ```sh
   docker-compose up -d --build
   ```
2. Для того чтобы ознакомиться с документацией и протестировать сервис, пройдите по ссылке 
   ```url
   http://127.0.0.1:8000/redoc
   ```
или
   ```url
   http://localhost:8000/docs
   ```
2. Для мониторинга и администрирования задач Celery в режиме реального времени, пройдите по ссылке 
   ```url
   http://localhost:5556
   ```

### Тестирование
Для запуска тестов, находясь в виртуальном окружении проекта, выполните команды
```sh
   pytest -v -s tests/
   ```
и
```sh
   pytest --cov .
   ```
Для генерации HTML-отчета в целях оценки покрытия тестами выполните команду
```sh
   pytest --cov=. --cov-report=html
   ```
