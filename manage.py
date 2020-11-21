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


def create_app():
  app = Flask(__name__)

  db = SQLAlchemy()
  db.init_app(app)

  seeder = FlaskSeeder()
  seeder.init_app(app, db)

  return app

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
    #medicines1 = medicines.Medicines(name='게보린', title= '치통', image_dir='image.jpg', effect='치통끝', capacity='2알', validity='2년', camera=False, users_id=1)
    schedules_common1 = schedules_common.Schedules_common(title='약', memo='먹기', startdate='3', enddate='5', cycle=2, schedules_ucommon=users1)
    #schedules_date1 = schedules_date.Schedules_date(year=1112, month=12, date=27, time='12:12:12', check=True, schedules_udate=users1, schedules_codate=schedules_common)

    # users2 = users.Users(full_name='abc', email='vvc@gmail.com', password='testtest12', mobile='123-1234-5678', login='basic')
    # medicines2 = medicines.Medicines(name='타이레놀', title= '두통', image_dir='fiel.jpg', effect='두통끝', capacity='1알', validity='1년', camera=False, users_id=2)
    # schedules_common2 = schedules_common.Schedules_common(title='약', users_id=2, memo='먹기', startdate='1', enddate='2', cycle=1)
    # schedules_date2 = schedules_date.Schedules_date(year=1111, month=11, date=27, time='12:12:12', check=True, users_id=2, schedules_common_id=2)

    db.session.add_all([users1, medicines1, schedules_common1, schedules_date1])
    db.session.commit()

if __name__ == '__main__':
 manager.run()
