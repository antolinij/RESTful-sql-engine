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
3. Build the container: `docker-compose build`
4. Run it: `docker-compose up -d`
5. Run the tests (Needs a running container): `docker-compose exec web python manage.py test`
6. You can run `docker-compose exec app bash` to have a shell inside the container.
7. Example to run a single test:  `docker-compose exec web python manage.py test api.tests.GetMovieTestCase`
8. after test remove images and volumes unused in docker `docker system prune -a`
