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

Before running any database script, you should create a database locally. Easiest way to do that is accessing the psql prompt and then creating a new database with:

```sh
create database wordfreq_dev
```

All database management is done trough the MigrateCommand extension. 
At the beginning, the process consists of three steps.

Fist, database is initialized with the `init` command:

```sh
python manage.py db init
```

Second, migrations are generated with the `migrate` command:

```sh
python manage.py db migrate
```

Finally, migrations are applied to the database with the `upgrade` command:

```sh
python manage.py db upgrade
```

Once all the steps are completed we can check the database tables as follows

```sh
psql wordfreq_dev
wordfreq_dev=# \dt
```

You should get something similar to the following:

```sh
            List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+-------
 public | alembic_version | table | username
 public | results         | table | username
(2 rows)
```


