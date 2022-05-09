Тестовое задание REST API для отслеживания карточек товаров Wildberries
=====

Функциональные требования:
----------
Методы проектируемого API должны обеспечивать следующие задачи:
 - добавление статьи (как сущности, к которой крепятся комментарии)
 - добавление комментария к статье
 - добавление коментария в ответ на другой комментарий (возможна любая вложенность)
 - получение всех комментариев к статье вплоть до 3 уровня вложенности
 - получение всех вложенных комментариев для комментария 3 уровня
 - по ответу API комментариев можно воссоздать древовидную структуру

Описание проекта
----------
Проект разворачивается в трех Docker контейнерах: web-приложение, postgresql-база данных и nginx-сервер.

В проекте реализована авторизация на базе JWT - токенов, настроена админка.

Настроены пермишены для эндпоинтов и пагинация для эндпоинта со статьями.

Приготовлены фикстуры для звполнения БД тестовыми данными (пароль и никнейм админа в фикстурах БД - ```admin```).

Системные требования
----------
* Python 3.6+
* Docker
* Works on Linux, Windows, macOS, BS

Стек технологий
----------
* Python 3.8
* Django 3.1
* Django Rest Framework
* Pytest
* PostreSQL
* Nginx
* gunicorn
* Docker
* Selery
* Redis
* BeautifulSoup4

Установка проекта из репозитория (Linux и macOS)
----------
1. Клонировать репозиторий и перейти в него в командной строке:
```bash 
git clone 'https://github.com/NikitaChalykh/API_Parcer_TW.git'

cd API_Parcer_TW
```

2. Cоздать и открыть файл ```.env``` с переменными окружения:
```bash 
cd infra

touch .env
```

3. Заполнить ```.env``` файл с переменными окружения по примеру:
```bash 
echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres >> .env

echo DB_HOST=db >> .env

echo DB_PORT=5432 >> .env
```

4. Установка и запуск приложения в контейнерах:
```bash 
docker-compose up -d
```

5. Запуск миграций, создание суперюзера, сбор статики и загрузка фикстур:
```bash 
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py collectstatic --no-input 

docker-compose exec web python manage.py loaddata fixtures.json
```
Документация к проекту
----------
Документация для API после установки доступна по адресу ```/redoc/```, ```/swagger/```.
