# EQ Author tool

## What is this?

EQ Author provides a rich web application, that acts as an Authoring tool for
surveys and questionaires. It enables a user to create and publish a questionaires
as part of a survey series, to be completed by a respondent (be they an organisation,
  individual or business).

This django web application has been designed to work in a 12 Factor apps pattern,
relying on the setting of certain environment variables to be able to
externalise settings and secret management, in accordance with GDS guidance.

## How to install

1. Create a new virtualenv
2. Activate the virtualenv
3. Clone this repo locally
4. Run `pip install -r requirements.txt`
5. To test for Heroku, use the heroku toolbelt: `heroku local` This will read
the procfile and run your django wsgi application.

## How to run the application 


## How to run the test suite

`manage.py test`

## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate


## Deployment via Docker compose
1. docker-compose build
2. docker-compose up

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [django-postgrespool](https://warehouse.python.org/project/django-postgrespool/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
