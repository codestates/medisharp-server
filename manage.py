import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_seeder import FlaskSeeder

from app.main import create_app, db
from app.main.model import users, medicines, schedules_common, schedules_date

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    # """Runs the unit tests."""
    # tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    # result = unittest.TextTestRunner(verbosity=2).run(tests)
    # if result.wasSuccessful():
    #     return 0
    # return 1
    users1 = users.Users(full_name='test', email='test@gmail.com', password='testtest', mobile='010-1234-5678', login='basic')
    # medicines1 = medicines(name='게보린', titl= '치통', image_dir='image.jpg', effect='치통끝', capacity='2알', validity='2년', camera=false, users_id=1)

    # users_medicines1 = users_medicines(users_id=1, medicines_id=1)

    db.session.add(users1)
    db.session.commit()


if __name__ == '__main__':
    manager.run()