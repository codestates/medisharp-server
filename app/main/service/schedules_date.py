#-*- coding: utf-8 -*-
#schedules_date 테이블에 관련된 쿼리문 작성하는 파일


from flask import request, jsonify, redirect
from sqlalchemy import and_
import json
from json import JSONEncoder
from app.main import db
from flask_restx import Resource, fields, marshal
from datetime import time


from app.main.model.schedules_date import Schedules_date
from app.main.model.users import Users

class TimeFormat(fields.Raw): #reference: https://stackoverflow.com/questions/46326075/specific-time-format-for-api-documenting-using-flask-restplus
    def format(self, value):
        return time.strftime(value, "%H:%M")


def get_monthly_checked(data): #req는 data{today:'yyyy-mm'}일 것 같음
  parsing = data['today'].split('-') #그러면 parsing = ['yyyy', 'mm', 'dd hh:mm:ss'] 일 것 같음
  year = parsing[0] #'yyyy'
  month = parsing[1] #'mm'
  
  user_id = 1 #이건 session을 확인해야하지만 일단 1로 하드코딩해 놓았음

  topic_fields = {
    'year': fields.Integer(required=True),
    'month': fields.Integer(required=True),
    'date': fields.Integer(required=True),
    'time': TimeFormat(readonly=True, description='Time in HH:MM', default='HH:MM'),
    'check': fields.Boolean(required=True),
  }


  return {'results': [marshal(topic, topic_fields) for topic in Schedules_date.query.filter(and_(Schedules_date.year==year, Schedules_date.month==month, Schedules_date.user_id==user_id)).all()]}

  
  












  # return jsonify(db.session.query(monthly_checked.year, Schedules_date.month, json.dumps(Schedules_date.time, default=str), Schedules_date.check).filter(Schedules_date.user_id==user_id).all()) 
  #Schedules_date.time 12:39:00 에서 계속 에러가 난다. 
  
  # try:
  #   response_object = {
  #     'status': 'OK',
  #     'message': 'Successfully get monthly checked.',
  #     'data': monthly_checked
  #   }
  #   return response_object, 200
  # except Exception as e:
  #   response_object = {
  #     'status': 'Internal Server Error',
  #     'message': 'Some Internal Server Error occurred.',
  #   }
  #   return response_object, 500
  






  