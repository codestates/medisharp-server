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