from flask_restx import Namespace, fields

class Schedules_dateDto:
  api = Namespace('schedules_date', description='Schedules_date Model for each alarms related (prescribed) medication')
  schedules_date = api.model('schedules_date', {
    #fields에 대해 궁금하다면 https://flask-restplus.readthedocs.io/en/stable/api.html 에서 한 중간쯤에 Model 부분에 나온다.
    'year': fields.Integer(required=True),
    'month': fields.Integer(required=True),
  })