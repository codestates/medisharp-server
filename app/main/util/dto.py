#dto는 data transfer object로 데이터를 전달하는 기능을 합니다.
from flask_restx import Namespace, fields

<<<<<<< HEAD

#User 데이터를 전달하는 함수를 만들어 줍니다.
=======
class Schedules_dateDto:
  api = Namespace('schedules_date', description='Schedules_date Model for each alarms related (prescribed) medication')
  schedules_date = api.model('schedules_date', {
    'year': fields.Integer(required=True, description='Year with alarm schedule'),
    'month': fields.Integer(required=True, description='Month with alarm schedule'),
    'date': fields.Integer(required=True, description='Date with alarm schedule'),
    'time': fields.String(required=True, description='Time(HH:MM:SS) with alarm schedule'),
    'check': fields.Boolean(required=True, description='Whether to take medicine on the day'),
  })

>>>>>>> 99ac0567ec5c8403832b79edf1acfee2cc089735
class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'full_name': fields.String(description='user full_name'),
        'password': fields.String(required=True, description='user password'),
        'mobile': fields.String(description='user mobile num'),
        'login': fields.String(required=True, description='user kind login')
    })