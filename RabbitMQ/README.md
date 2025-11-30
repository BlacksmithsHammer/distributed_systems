# RabbitMQ Producer-Consumer Application

Приложение демонстрирует работу с RabbitMQ: генерация задач, маршрутизация, обработка и Dead Letter Queue.

## Описание

- Producer: генерирует математические задачи и отправляет в RabbitMQ
- Consumer: обрабатывает задачи, выполняет вычисления
- DLQ: неудачные задачи (деление на ноль, неизвестные операции) попадают в Dead Letter Queue

## Операции

- add: сложение
- subtract: вычитание
- multiply: умножение
- divide: деление (может быть деление на ноль)
- power: возведение в степень
- invalid: неизвестная операция (всегда падает)

## Структура проекта

    producer/
        app.py
        requirements.txt
        Dockerfile
    consumer/
        app.py
        requirements.txt
        Dockerfile
    docker-compose.yml
    README.md

## Требования

- Docker
- Docker Compose

## Запуск

Сборка и запуск:

    docker-compose up --build -d

Просмотр логов всех сервисов:

    docker-compose logs -f

Просмотр логов producer:

    docker-compose logs -f producer

Просмотр логов consumer:

    docker-compose logs -f consumer consumer2

## Тестирование

Открыть RabbitMQ Management UI:

    http://localhost:15672
    Login: admin
    Password: admin123

Проверить очереди:

- calc_queue: основная очередь задач
- dlq_queue: очередь неудачных задач

Наблюдение за обработкой:

    docker-compose logs -f consumer consumer2

Пример успешной обработки в логах:

    [RECEIVED] Task 1234: add(50, 30)
    [SUCCESS] Task 1234: add(50, 30) = 80

Пример неудачной обработки:

    [RECEIVED] Task 5678: divide(42, 0)
    [FAILED] Task 5678: divide(42, 0) - Error: Division by zero
    [DLQ] Rejecting task 5678 to Dead Letter Queue

Пример неизвестной операции:

    [RECEIVED] Task 9999: invalid(10, 20)
    [FAILED] Task 9999: invalid(10, 20) - Error: Unknown operation: invalid
    [DLQ] Rejecting task 9999 to Dead Letter Queue

## Масштабирование

Добавить больше consumer:

    docker-compose up -d --scale consumer=3

## Полезные команды

Статус контейнеров:

    docker-compose ps

Перезапуск producer:

    docker-compose restart producer

Остановка:

    docker-compose down

Остановка с удалением данных:

    docker-compose down -v

Пересборка без кэша:

    docker-compose build --no-cache

## Архитектура

    Producer -> [calc_exchange] -> [calc_queue] -> Consumer
                                         |
                                    (on failure)
                                         |
                                         v
                               [dlx_exchange] -> [dlq_queue]

Сообщения отправляются в calc_exchange с routing_key='calculate'.
Consumer обрабатывает сообщения из calc_queue.
При ошибке сообщение reject без requeue, попадает в DLQ через Dead Letter Exchange.

## Технологии

- Python 3.11
- Pika (RabbitMQ client)
- RabbitMQ 3.12
- Docker / Docker Compose
