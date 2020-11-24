#서버 실행시 여기가 1번 실행 입니다. 그릐고 main/__init__.py로 가요

import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model import users, medicines, schedules_common, schedules_date

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint) #이 코드 꼭 추가해주세요. 라우팅에 필요합니다. 없으니 안되더라구요

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()

@manager.command
def test():

    my_schedules_date = schedules_date.Schedules_date(year=2020, month=11, date=22, time='12:39:00', check=True)
    my_schedules_common = schedules_common.Schedules_common(title='처방받은 수면제', memo='자기전에 꼭 먹어!', startdate='6', enddate='15', cycle=2)
    my_users = users.Users(full_name='Grace', email='hjngy0511@gmail.com', password='qwerty12345', mobile='010-1234-5678', login='basic')
    my_medicines = medicines.Medicines(name='잘자정', title= '수면유도제', image_dir='sleepfile.jpg', effect='불면 끝', capacity='1알', validity='일주일', camera=False)
    
    my_users.schedules_commons.append(my_schedules_common)
    my_users.schedules_dates.append(my_schedules_date)
    my_schedules_common.schedules_dates.append(my_schedules_date)
    db.session.add(my_users)
    db.session.add(my_medicines)
    db.session.add(my_schedules_common)
    db.session.add(my_schedules_date)
    my_medicines.taker.append(my_users)
    my_schedules_common.ttt.append(my_medicines)
   
    db.session.commit()







if __name__ == '__main__':
    manager.run()