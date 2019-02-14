import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

# Configure app
app.config.from_object(os.environ['APP_SETTINGS'])

# Create migrate object
# It allows to create a migration repository (migrations folder) with `flask db init`
# And then generate an initial migration with `flask db migrate`
migrate = Migrate(app, db)

# Create a manager
# Commands are executed with `python manage.py command`
# For example, to run the app use 'python manage.py runserver`
manager = Manager(app)

# Add new migrate command to the manager object, named db
# It allos the execute flask db commands from the manager: `python manage.py db init`
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()