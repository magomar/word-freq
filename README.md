# Word Frequency

Web app using Flask that calculates word-frequency pairs based on the text from a given URL.
This project is the output the tutorial [Flask By Example](https://realpython.com/flask-by-example-part-1-project-setup/).

That tutorial addresses the creation and deploying of a flask app on Heroku using multiple configurations (development, testing, staging, production)

In particular, two projects are created on Heroku, with two separate configurations:

```shell
heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
```

For data storage, this app uses a **PostgreSQL** database and an Object Relational Mapping framework, **SQLAlchemy**. Results of the word frequency computation are store in objects with the following structure

Note the use of the JSON datatype for certain columns of the database.

To migrate changes in the data model it uses **Alembic**, which is part of Flask-Migrate.

## Basic usage

Database is initialized with:

```sh
python manage.py db init
```