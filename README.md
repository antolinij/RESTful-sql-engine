# RESTful-sql-engine

Api in Google docs [here](https://docs.google.com/document/d/1xWNwTG2UidBcYzd6nQ6HZPGU9G1JBuzk2saYPcDkCUQ/edit?usp=sharing)

## Tech Stack
In this repo you'll find a simple implementation of a Flask API server. The tech stack we're using is this:


* Database: PostgreSQL 11
* Django: 3.0
* Django Rest Framework: 3.12.4
* Docker-compose
* Unittest integrated in drf

## How to install and run tests
To install the project you should just use basic docker-compose commands.

1. Clone this repository
2. Create two files (.env y .env.db) with credentials for django and postgresql. See note #1 an example at the end of this readme.
3. Build the container: `docker-compose build`
4. Run it: `docker-compose up -d`
5. Run the tests (Needs a running container): `docker-compose exec web python manage.py test`
6. You can run `docker-compose exec app bash` to have a shell inside the container.
7. Example to run a single test:  `docker-compose exec web python manage.py test api.tests.GetMovieTestCase`
8. after test remove images and volumes unused in docker `docker system prune -a`

## note #1 These files have to be in the folder as the docker-compose.yml file
# you should choose your own data 
# .env:
DEBUG=0
SECRET_KEY=asd123sadfas234JH7DDFs3
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=ine
SQL_USER=ine_user
SQL_PASSWORD=super_secreta1234
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres

# .env.db:
POSTGRES_USER=ine_user
POSTGRES_PASSWORD=super_secreta1234
POSTGRES_DB=ine

