#-*- coding: utf-8 -*-
# medicines 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_
import json
import jwt
import datetime
from operator import itemgetter
from app.main import db
from app.main.model.schedules_common import Schedules_common
from app.main.model.schedules_date import Schedules_date
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg
import re

def post_schedules_common(data):
  """ Post Common information of alarm"""
  try:
    try: 
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
      if decoded_token:
        new_schedules_common = Schedules_common(
          title=data['title'], 
          memo=data['memo'],
          startdate=data['startdate'],
          enddate=data['enddate'],
          cycle=data['cycle'],
          user_id=user_id,
          )
        db.session.add(new_schedules_common)
        db.session.commit() 
        
        results = {
          "new_schedules_common_id": new_schedules_common.id,
          "time": data['time'], 
          "startdate" : new_schedules_common.startdate,
          "enddate" : new_schedules_common.enddate,
          "cycle" : new_schedules_common.cycle
        }
        response_object = {
          'status': 'OK',
          'message': 'Successfully Post Common information of alarm.',
          'results': results
        }
        return response_object, 200
    except Exception as e:  
      print(e)
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


def post_schedules_date(data):
  """ Post Schedules Date API"""
  try:
    # medicine_id = data['medicines_id']
    schedules_common_id = data['schedules_common_id']
    startdate=datetime.datetime.strptime(data['startdate'], '%Y-%m-%d')
    enddate=datetime.datetime.strptime(data['enddate'], '%Y-%m-%d')
    cycle=data['cycle']
    # time = data['time']
    print(data)

    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      if decoded_token:
        print(user_id)

        #result = db.session.query(Schedules_common.startdate, Schedules_common.enddate, Schedules_common.cycle).filter(and_(Schedules_common.id==schedules_common_id, Schedules_common.user_id==user_id)).all() 
        #일단 startdate, enddate 형변환 
        #print(result)
        #print(result[0])
        # startdate = datetime.datetime.strptime(result[0].startdate, '%Y-%m-%d')
        # enddate = datetime.datetime.strptime(result[0].enddate, '%Y-%m-%d')
        # cycle = result[0].cycle #2
        #print(startdate, enddate, cycle)
        
        #비교연산자로 기저조건을 걸어주고 주기 계산
        currdate = startdate
        while currdate <= enddate:
          #이를 schedules_date 테이블에 넣어주기
          new_schedules_date = Schedules_date(
            alarmdate = currdate,
            time = data['time'],
            check = 0,
            user_id = user_id,
            schedules_common_id = schedules_common_id
          )
          db.session.add(new_schedules_date)
          db.session.commit()
          currdate = currdate + datetime.timedelta(days=cycle)

        #response는 medicine_id와 schedules_common_id
        results = {
          'medicine_id': data['medicines_id'],
          'schedules_common_id': schedules_common_id
        }

        response_object = {
          'status': 'OK',
          'message': 'Successfully post schedules date.',
          'results': results
        }
        return response_object, 200

    except Exception as e:
        print(e)
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


def get_schedules_common(data):
  """ Get Common information of alarm"""
  try:
    schedules_common_id =data['schedules_common_id']

    try: 
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      if decoded_token:
        topic_fields = {
          'startdate': fields.String(required=True),
          'enddate': fields.String(required=True),
          
        }
        res_date = [marshal(topic, topic_fields) for topic in Schedules_common.query
                                                                        .filter(and_(Schedules_common.id == schedules_common_id,Schedules_common.user_id==user_id))
                                                                        .all()]
        results = []
        result = {
          'schedules_common_id' : schedules_common_id,
          'title' : data['title'],
          'startdate': res_date[0]['startdate'],
          'enddate': res_date[0]['enddate'],
          'cycle': data['cycle'],
          'memo': data['memo'],
          'time': data['time'],
          'check': data['check']
        }
        results.append(result)
        response_object = {
          'status': 'OK',
          'message': 'Successfully get schedule common info.',
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
