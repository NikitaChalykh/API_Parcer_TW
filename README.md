REST API for tracking Wildberries product cards
=====

Functional requirements
----------
* Automatic tracking of the dynamics of changes in the parameters of the product card on
Marketplace Wildberries
* Receipt on request of statistical
information about the state of the card parameters in the specified range of dates from
specified time interval (no more than 1 record per hour).

Project Description
----------
The project is deployed in the following Docker containers: web application, postgresql database, nginx server, Redis database, and Celery container.

Implemented authentication based on JWT tokens, configured the admin panel, implemented testing of the main models and urls of the project. Information about the historical state of product cards is filtered by date range with intervals.

The data collection task is implemented as asynchronous Celery tasks.

Fixtures are prepared for filling the database with test data. The password and nickname of the admin in the database fixtures is ```admin```.

System requirements
----------
* Python 3.6+
* Docker
* Works on Linux, Windows, macOS, BS

Technology stack
----------
* Python 3.8
* Django 3.1
* Django Rest Framework
* unittest
* PostreSQL
* Nginx
* gunicorn
* Docker
* Сelery
* Redis
* BeautifulSoup4

Installing a project from a repository (Linux and macOS)
----------
1. Clone the repository and go to it on the command line:
```bash
git clone git@github.com:NikitaChalykh/API_Parcer_TW.git

cd API_Parcer_TW
```

2. Create and open the ```.env``` file with environment variables:
```bash
cd infrared

touch.env
```

3. Fill in the ```.env``` file with environment variables as follows:
```bash 
echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres >> .env

echo DB_HOST=db >> .env

echo DB_PORT=5432 >> .env

echo BROKER=redis://redis >> .env

echo BROKER_URL=redis://redis:6379/0 >> .env
```

4. Installing and Running an Application in Containers:
```bash 
docker-compose up -d
```

5. Running migrations, collecting statics, loading fixtures and running tests:
```bash 
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py collectstatic --no-input 

docker-compose exec web python manage.py loaddata fixtures.json

docker-compose exec web python manage.py test 
```
Project Documentation
----------
Documentation for the API after installation is available at:

```http://127.0.0.1/redoc/```

```http://127.0.0.1/swagger/```
