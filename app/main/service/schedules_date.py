#-*- coding: utf-8 -*-
#schedules_date 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_
import json
import jwt
import re
import datetime
from operator import itemgetter
from app.main import db
from app.main.model.schedules_date import Schedules_date
from app.main.model.schedules_common import Schedules_common
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg
import re

class TimeFormat(fields.Raw):
    def format(self, value):
        return datetime.time.strftime(value, "%H:%M")

class DateFormat(fields.Raw):
    def format(self, value):
        return datetime.datetime.strftime(value, "%d")

def sorting_alarmdate_time(data):
  """ date로 오름차순 정렬 후 time으로 오름차순 정렬하는 함수 """
  data = sorted(data, key=itemgetter('alarmdate', 'time'))
  return data

def sorting_time(data):
  """ time으로 오름차순 정렬하는 함수 """
  data = sorted(data, key=itemgetter('time'))
  return data


def get_monthly_checked(data): 
  """ Get monthly checked API for calendar"""
  try: 
    start_day = datetime.datetime.strptime(data['start_day'], '%Y-%m-%d')
    end_day = datetime.datetime.strptime(data['end_day'], '%Y-%m-%d')
    try: 
      user_id = 1
      # token = request.headers.get('Authorization')
      # decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      # user_id = decoded_token['id']
      # if decoded_token:
      if user_id:
        topic_fields = {
          'alarmdate': DateFormat(readonly=True, description='Date in DD', default='DD'),
          'time': TimeFormat(readonly=True, description='Time in HH:MM', default='HH:MM'),
          'check': fields.Boolean(required=True),
        }
        data = [marshal(topic, topic_fields) for topic in Schedules_date.query
                                                                        .filter(and_(Schedules_date.alarmdate>=start_day, Schedules_date.alarmdate<end_day, Schedules_date.user_id==user_id))
                                                                        .all()]
        results = sorting_alarmdate_time(data)
        response_object = {
          'status': 'OK',
          'message': 'Successfully get monthly checked.',
          'results': results
        }
        return response_object, 200
    except Exception as e:
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


"""
client가 params에 
today: 2020-11-22 12:23:00
와 같은 형태로 get 요청을 한다는 가정하에 구현
"""
def get_alarms_list(data): 
  """ Get Alarms List on Clicked date for main page and calendar page"""
  try:
    parsing = re.split('-| ', data['date']) 
    year = parsing[0] 
    month = parsing[1] 
    date = parsing[2]

    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token, jwt_key, jwt_alg)
    user_id = decoded_token['id']

    if decoded_token:
      """
      schedules_date와 schedules_common을 innerjoin하여서 
      schedules_date에서는 check, time
      schedules_common에서는 title, cycle, memo
      데이터를 가져와야한다. 
      """
      # reference: https://www.youtube.com/watch?v=_HIY1lZKEw0
      data = db.session.query(Schedules_date.check, Schedules_date.time, Schedules_common.title, Schedules_common.cycle, Schedules_common.memo).filter(and_(Schedules_date.schedules_common_id == Schedules_common.id, Schedules_date.year==year, Schedules_date.month==month,Schedules_date.date==date, Schedules_date.user_id==user_id)).all() 

      results = []
      for el in data:
        result = {}
        result['check'] = el.check
        result['time'] = time.strftime(el.time, "%H:%M")
        result['title'] = el.title
        result['cycle'] = el.cycle
        result['memo'] = el.memo
        results.append(result)

      results = sorting_time(results)
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

    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token, jwt_key, jwt_alg)
    user_id = decoded_token['id']

    if decoded_token:
      topic_fields = {
        'check': fields.Boolean(required=True),
      }
      data = [marshal(topic, topic_fields) for topic in Schedules_date.query.filter(and_(Schedules_date.year.between(start_day_parsing[0], end_day_parsing[0]), Schedules_date.month.between(start_day_parsing[1], end_day_parsing[1]), Schedules_date.date.between(start_day_parsing[2], end_day_parsing[2]), Schedules_date.user_id==user_id)).all()]
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

