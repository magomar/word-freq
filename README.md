# Word Frequency

Web app using Flask that calculates word-frequency pairs based on the text from a given URL.
This project is the output the tutorial [Flask By Example](https://realpython.com/flask-by-example-part-1-project-setup/).

That tutorial addresses the creation and deploying of a flask app on Heroku using multiple configurations (development, testing, staging, production)

For data storage, this app uses a **PostgreSQL** database and an Object Relational Mapping framework, **SQLAlchemy**. Results of the word frequency computation are store in objects with the following structure

Note the use of the JSON datatype for certain columns of the database.

To migrate changes in the data model it uses **Alembic**, which is part of Flask-Migrate.

## Heroku

The Heroku platform uses a container model to run and scale all Heroku apps. Heroku containers are called **dynos**. Dynos are isolated, virtualized Linux containers that are designed to execute code based on a user-specified command.

Heroku apps include a **Procfile** that specifies the commands that are executed by the app on startup. You can use a Procfile to declare a variety of process types, including:

- Your app’s web server
- Multiple types of worker processes
- A singleton process, such as a `clock`
- Tasks to run before a new release is deployed

Each dyno in your app belongs to one of the declared process types, and it executes the startup command associated with that process type.

For our project we need a **web** server process type, and in particular, for Python apps Heroku recommends **Gunicorn**. So we specify web as our process type and [gunicorn](https://gunicorn.org/) as the specific web server in the Procfile, as follows:

    web: gunicorn app:app

Heroku apps can use source code from Github, but they can also host code at the Heroku servers. An easy way to create Heroku apps is through thye Heroku CLI, which can be installed with:

    curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

Apps are created with command create

```sh
heroku create yourapp
```

It is possible to create two apps for the same project, one for staging (development phase), another one for production.

```sh
heroku create yourapp-stage
heroku create yourapp-prod
```

When using that approach to create Heroku apps, each app will have each own git repository, so they can both be added as remotes to your local git repository:

```sh
git remote add stage git@heroku.com:yourapp-stage.git
git remote add pro git@heroku.com:yourapp-pro.git
```

Now we can push both of our apps live to Heroku.

- For staging: git push stage master
- For production: git push pro master

We can execute the apps manually using 

We need to establish different environments according to the instance we are running: *production* or *staging*. To do that we can define a single configuration file (`config.py`) with the following line

```python
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
```

And then, we set the proper `Config` class using environment variables. Environment variables for Heroku apps can be define though the web interface or using the Heroku CLI. In our example, we will setup the appropiate `Config` class with:

```sh
heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
```

Finally, we can run our apps from the Heroku CLI with

```sh
heroku run python app.py --app yourapp-stage
```

## Database

## Local setup

It is possible to create a database locally by accessing the Postgres prompt and then creating a new database with:

```sh
sudo -u postgres psql
postgres-# create database wordfreq_dev
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

You can also check the content of the results database with:

```sh
wordfreq_dev=# \d results
```

And that will produce the output below:

```sh
                                        Table "public.results"
        Column        |       Type        | Collation | Nullable |               Default               
----------------------+-------------------+-----------+----------+-------------------------------------
 id                   | integer           |           | not null | nextval('results_id_seq'::regclass)
 url                  | character varying |           |          | 
 result_all           | json              |           |          | 
 result_no_stop_words | json              |           |          | 
Indexes:
    "results_pkey" PRIMARY KEY, btree (id)
```

## Remote migration

First, we need to add the Postgress addon to the staging server. If we are using a free-tierm then the appropiate add-on is called hobby-dev

```sh
heroku addons:create heroku-postgresql:hobby-dev --app yourapp-stage
```

We can check that a database connection have been created with

```sh
heroku config --app yourapp-stage
```

And the output will be something like this:

```sh
=== yourapp-stage Config Vars
APP_SETTINGS: config.StagingConfig
DATABASE_URL: postgres://some_long_url...
```

Finally, we can execute the migration remotely with:

    heroku run python manage.py db upgrade --app yourapp-stage

And now, we can repeat the latest steps with the production app:

```sh
heroku addons:create heroku-postgresql:hobby-dev --app yourapp-stage
heroku run python manage.py db upgrade --app yourapp-stage
```