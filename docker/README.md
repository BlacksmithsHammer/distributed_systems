# Docker Containerization Demo

Демонстрационный проект контейнеризации: Flask API + PostgreSQL в Docker-сети с персистентным хранением данных.

## Описание

Проект состоит из двух Docker-контейнеров:

- API — Flask-приложение (точка входа), порт 5000
- Database — PostgreSQL база данных, порт 5432

Данные сохраняются при перезапуске контейнеров благодаря Docker Volume.

## Структура проекта

    docker-compose.yml
    api/
        Dockerfile
        requirements.txt
        app.py
    db/
        init.sql
    README.md

## Требования

- Docker 20.10+
- Docker Compose 2.0+

## Запуск

Сборка и запуск:

    docker-compose up --build -d

Остановка:

    docker-compose down

Остановка с удалением данных:

    docker-compose down -v

Просмотр логов:

    docker-compose logs -f

## API Endpoints

- GET / — информация об API
- GET /health — проверка здоровья
- GET /users — список пользователей
- POST /users — создать пользователя
- GET /products — список продуктов
- POST /products — создать продукт
- GET /stats — статистика БД

## Примеры запросов

Проверка работоспособности:

    curl http://localhost:5000/health

Получить пользователей:

    curl http://localhost:5000/users

Создать пользователя:

    curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"username": "new_user", "email": "new@example.com"}'

Получить продукты:

    curl http://localhost:5000/products

Создать продукт:

    curl -X POST http://localhost:5000/products -H "Content-Type: application/json" -d '{"name": "Monitor", "price": 25000, "quantity": 5}'

Статистика:

    curl http://localhost:5000/stats

## Проверка персистентности данных

Создаём пользователя:

    curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"username": "persist_test", "email": "test@test.com"}'

Перезапускаем контейнеры:

    docker-compose down
    docker-compose up -d
    sleep 10

Проверяем — пользователь на месте:

    curl http://localhost:5000/users

## Полезные команды

Статус контейнеров:

    docker-compose ps

Зайти в БД:

    docker exec -it my_database psql -U admin -d myapp

SQL запрос напрямую:

    docker exec -it my_database psql -U admin -d myapp -c "SELECT * FROM users;"

## Технологии

- Python 3.11
- Flask 3.0
- PostgreSQL 15
- Docker / Docker Compose
