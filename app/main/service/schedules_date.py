#-*- coding: utf-8 -*-
#schedules_date 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_
import json , jwt, re, datetime
from operator import itemgetter
from app.main import db
from app.main.model.schedules_date import Schedules_date
from app.main.model.schedules_common import Schedules_common
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg

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

def response_err():
  response_object = {
    'status': 'fail',
    'message': 'Provide a valid auth token.',
  }
  return response_object


def get_monthly_checked(data, user_id): 
  """ Get monthly checked API for calendar"""
  try: 
    start_day = datetime.datetime.strptime(data['startDay'], '%Y-%m-%d')
    end_day = datetime.datetime.strptime(data['endDay'], '%Y-%m-%d')
    topic_fields = {
      'alarmdate': DateFormat(readonly=True, description='Date in DD', default='DD'),
      'time': TimeFormat(readonly=True, description='Time in HH:MM', default='HH:MM'),
      'check': fields.Boolean(required=True),
    }
    data = [marshal(topic, topic_fields) for topic in Schedules_date.query
                                                                    .filter(and_(Schedules_date.alarmdate>=start_day, Schedules_date.alarmdate<end_day, Schedules_date.user_id==user_id))
                                                                    .all()]
    return sorting_alarmdate_time(data)
  except Exception as e:
    return response_err(), 401


def get_alarms_list(data, user_id): 
  """ Get Alarms List on Clicked date for main page and calendar page"""
  try:
    alarmdate = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
    data = db.session.query(Schedules_common.id,Schedules_common.title, Schedules_common.cycle, Schedules_common.memo, Schedules_date.time, Schedules_date.check, Schedules_date.push).join(Schedules_common).filter(and_(Schedules_date.alarmdate==alarmdate, Schedules_date.user_id==user_id)).all()
    results = []
    for el in data:
      result = {}
      result['schedules_common_id'] = el.id
      result['title'] = el.title
      result['cycle'] = el.cycle
      result['memo'] = el.memo
      result['time'] = datetime.time.strftime(el.time, "%H:%M")
      result['check'] = el.check
      result['push'] = el.push
      results.append(result)
    return sorting_time(results)
  except Exception as e:
    return response_err(), 401


def get_today_checked(data, user_id): 
  """ Get today checked API for calendar"""
  try: 
    start_day = datetime.datetime.strptime(data['startDay'], '%Y-%m-%d')
    end_day = datetime.datetime.strptime(data['endDay'], '%Y-%m-%d')
    topic_fields = {
      'check': fields.Boolean(required=True),
    }
    data = [marshal(topic, topic_fields) for topic in Schedules_date.query
                                                                    .filter(and_(Schedules_date.alarmdate.between(start_day, end_day), Schedules_date.user_id==user_id))
                                                                    .all()]                                                                     
    return data
  except Exception as e:
    return response_err(), 401


def patch_check(data, user_id):
  """ Convert check False to True or True to False"""
  try:
    schedules_common_id = data['schedules_common_id']
    alarmdate = datetime.datetime.strptime(data['clickdate'], '%Y-%m-%d')
    this_schedules_date = db.session.query(Schedules_date).filter(and_(Schedules_date.schedules_common_id==schedules_common_id,Schedules_date.alarmdate==alarmdate,Schedules_date.user_id==user_id)).first()
    if this_schedules_date.check == True:
      this_schedules_date.check = False
    else:
      this_schedules_date.check = True
    return {'check': this_schedules_date.check}
  except Exception as e:  
    return response_err(), 401