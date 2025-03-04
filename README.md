Сервис отслеживания карточек товаров маркетплейса Wildberries
=====

Описание проекта
----------
Сервис предназначен для автоматического отслеживания изменений параметров карточек товаров на маркетплейсе Wildberries. Сервис позволяет получать статистические данные о состоянии карточек в заданном диапазоне дат с учетом временного интервала обновления (не чаще 1 записи в час).

Проект разворачивается в следующих Docker контейнерах: web-приложение, postgresql-база данных, nginx-сервер, Redis-база данных и Celery-контейнер.

Реализована аутентификация на базе JWT-токенов, настроена админка, реализовано тестирование основных моделей и url-ов проекта. Информация об историческом состоянии карточек товаров фильтруется по диапазону дат с интервалами.

Отслеживание данных карточек реализовано в виде асинхронной Celery задачи.

Приготовлены фикстуры для заполнения БД тестовыми данными. Пароль и никнейм админа в фикстурах БД - ```admin```.

Системные требования
----------
* Python 3.8+
* Docker
* Works on Linux

Стек технологий
----------
* Python 3.8+
* Django 3.1
* Django Rest Framework
* unittest
* PostreSQL
* Nginx
* gunicorn
* Docker, Docker Compose
* Сelery
* Redis
* BeautifulSoup4

Установка проекта из репозитория
----------
1. Клонирование репозитория:
```bash
git clone git@contest.idacloud.ru:Nikita223/marketplace_product_tracking_service.git

cd marketplace_product_tracking_service # Переходим в директорию с проектом
```

2. Создайте файл ```.env``` используя ```env.example``` в качестве шаблона в папке infra

3. Установка и запуск приложения в контейнерах:
```bash 
docker-compose up -d
```

4. Запуск миграций, сбор статики, загрузка фикстур и запуск тестов:
```bash 
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py collectstatic --no-input 

docker-compose exec web python manage.py loaddata fixtures.json

docker-compose exec web python manage.py test 
```

Работа с проектом
----------
Документация по работе API сервиса:

```http://127.0.0.1/redoc/```

```http://127.0.0.1/swagger/```

Админка сервиса:

```http://127.0.0.1/admin/```
