#-*- coding: utf-8 -*-
#schedules_date 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_
import json
import jwt
from datetime import time
from operator import itemgetter
from app.main import db
from app.main.model.schedules_date import Schedules_date
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg
import re

class TimeFormat(fields.Raw):
    def format(self, value):
        return time.strftime(value, "%H:%M")

def sorting_date_time(data):
  """ date로 오름차순 정렬 후 time으로 오름차순 정렬하는 함수 """
  data = sorted(data, key=itemgetter('date', 'time'))
  return data

def get_monthly_checked(data): 
  """ Get monthly checked API for calendar"""
  try:
    parsing = data['today'].split('-') 
    year = parsing[0] 
    month = parsing[1] 

    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token, jwt_key, jwt_alg)
    user_id = decoded_token['id']

    if decoded_token:
      topic_fields = {
        'date': fields.Integer(required=True),
        'time': TimeFormat(readonly=True, description='Time in HH:MM', default='HH:MM'),
        'check': fields.Boolean(required=True),
      }
      data = [marshal(topic, topic_fields) for topic in Schedules_date.query.filter(and_(Schedules_date.year==year, Schedules_date.month==month, Schedules_date.user_id==user_id)).all()]
      results = sorting_date_time(data)
      response_object = {
        'status': 'OK',
        'message': 'Successfully get monthly checked.',
        'results': results
      }
      return response_object, 200
    else:
      response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.',
      }
      return response_object, 401

  except Exception as e:
    response_object = {
      'status': 'Internal Server Error',
      'message': 'Some Internal Server Error occurred.',
    }
    return response_object, 500



def get_today_checked(data): 
  """ Get today checked API for calendar"""
  try:
    start_day_parsing = re.split('-| ', data['start_day']) 
    end_day_parsing = re.split('-| ', data['end_day']) 

    # token = request.headers.get('Authorization')
    # decoded_token = jwt.decode(token, jwt_key, jwt_alg)
    # user_id = decoded_token['id']
    user_id = 1

    #if decoded_token:
    if user_id:
      topic_fields = {
        'check': fields.Boolean(required=True),
      }
      data = [marshal(topic, topic_fields) for topic in Schedules_date.query.filter(and_(Schedules_date.year.between(start_day_parsing[0], end_day_parsing[0]), Schedules_date.month.between(start_day_parsing[1], end_day_parsing[1]), Schedules_date.date.between(start_day_parsing[2], end_day_parsing[2]), Schedules_date.user_id==user_id)).all()]
      print(data)
      response_object = {
        'status': 'OK',
        'message': 'Successfully get today checked.',
        'results': data
      }
      return response_object, 200
    else:
      response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.',
      }
      return response_object, 401

  except Exception as e:
    response_object = {
      'status': 'Internal Server Error',
      'message': 'Some Internal Server Error occurred.',
    }
    return response_object, 500


