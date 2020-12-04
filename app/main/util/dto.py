#dto는 data transfer object로 데이터를 전달하는 기능을 합니다.
from flask_restx import Namespace, fields

class Schedules_dateDto:
  api = Namespace('schedules_date', description='Schedules_date Model for each alarms related (prescribed) medication')
  schedules_date = api.model('schedules_date', {
    'year': fields.Integer(required=True, description='Year with alarm schedule'),
    'month': fields.Integer(required=True, description='Month with alarm schedule'),
    'date': fields.Integer(required=True, description='Date with alarm schedule'),
    'time': fields.String(required=True, description='Time(HH:MM:SS) with alarm schedule'),
    'check': fields.Boolean(required=True, description='Whether to take medicine on the day'),
  })

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'full_name': fields.String(description='user full_name'),
        'password': fields.String(required=True, description='user password'),
        'mobile': fields.String(description='user mobile num'),
        'login': fields.String(required=True, description='user kind login')
    })

class Schedules_commonDto:
  api = Namespace('schedules_common', description='Schedules_common Model for total periods of alarms related (prescribed) medication')
  schedules_common = api.model('schedules_common', {
    'title': fields.String(required=True, description='Name indicating the medicine you need to take'),
    'memo': fields.String(required=True, description='Description of the alarm'),
    'startdate': fields.Integer(required=True, description='Alarm start date'),
    'enddate': fields.Integer(required=True, description='Alarm end date'),
    'cycle': fields.Integer(required=True, description='Alarm cycle'),
  }) 