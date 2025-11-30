# Kubernetes Backend-Frontend Application

Демонстрация деплоя backend-frontend приложения в Kubernetes.

## Описание

- Backend: Flask API, внутренний порт 5000, реплицирован (3 реплики)
- Frontend: Flask веб-приложение, внешний порт 30080, проксирует запросы к backend

## Структура проекта

    backend/
        app.py
        requirements.txt
        Dockerfile
    frontend/
        app.py
        requirements.txt
        Dockerfile
    k8s/
        backend-deployment.yaml
        backend-service.yaml
        frontend-deployment.yaml
        frontend-service.yaml
    README.md

## Требования

- Docker
- Minikube или другой Kubernetes кластер
- kubectl

## Запуск

1. Запустить Minikube:

        minikube start

2. Использовать Docker daemon Minikube:

        eval $(minikube docker-env)

3. Собрать образы:

        docker build -t backend:latest ./backend
        docker build -t frontend:latest ./frontend

4. Применить Kubernetes манифесты:

        kubectl apply -f k8s/backend-deployment.yaml
        kubectl apply -f k8s/backend-service.yaml
        kubectl apply -f k8s/frontend-deployment.yaml
        kubectl apply -f k8s/frontend-service.yaml

5. Проверить статус:

        kubectl get pods
        kubectl get services

6. Получить URL для доступа:

        minikube service frontend-service --url

## Тестирование

Получить URL:

    export FRONTEND_URL=$(minikube service frontend-service --url)

Открыть в браузере:

    echo $FRONTEND_URL

Проверка через curl:

    curl $FRONTEND_URL
    curl $FRONTEND_URL/health
    curl $FRONTEND_URL/api/backend/data

Проверка балансировки (выполнить несколько раз, hostname будет меняться):

    curl $FRONTEND_URL/api/backend/data
    curl $FRONTEND_URL/api/backend/data
    curl $FRONTEND_URL/api/backend/data

## Полезные команды

Список подов:

    kubectl get pods -o wide

Логи backend:

    kubectl logs -l app=backend

Логи frontend:

    kubectl logs -l app=frontend

Описание сервисов:

    kubectl describe service backend-service
    kubectl describe service frontend-service

Масштабирование backend:

    kubectl scale deployment backend-deployment --replicas=5

Удаление всех ресурсов:

    kubectl delete -f k8s/

Остановка Minikube:

    minikube stop

## Архитектура

Frontend Service (NodePort:30080) -> Frontend Pods -> Backend Service (ClusterIP:5000) -> Backend Pods (3 replicas)

Внешний трафик поступает на Frontend через NodePort.
Frontend проксирует запросы к Backend через внутренний ClusterIP сервис.
Backend реплицирован, нагрузка распределяется между подами.

## Технологии

- Python 3.11
- Flask 3.0
- Docker
- Kubernetes
- Minikube
