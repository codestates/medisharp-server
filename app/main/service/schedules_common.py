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
from sqlalchemy.sql.functions import now

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
          "time": data['time']
        }
        response_object = {
          'status': 'OK',
          'message': 'Successfully Post Common information of alarm.',
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


def post_schedules_date(data):
  """ Post Schedules Date API"""
  try:
    medicine_id = data['medicine_id']
    schedules_common_id = data['schedules_common_id']
    time = data['time']

    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      if decoded_token:
        data = db.session.query(Schedules_common.startdate, Schedules_common.enddate, Schedules_common.cycle).filter(and_(Schedules_common.id==schedules_common_id, Schedules_common.user_id==user_id)).all() 
        #일단 startdate, enddate 형변환 
        startdate = datetime.datetime.strptime(data[0].startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(data[0].enddate, '%Y-%m-%d')
        cycle = data[0].cycle #2
        print(startdate, enddate, cycle)
        
        #비교연산자로 기저조건을 걸어주고 주기 계산
        currdate = startdate
        while currdate <= enddate:
          #이를 schedules_date 테이블에 넣어주기
          new_schedules_date = Schedules_date(
            alarmdate = currdate,
            time = time,
            check = 0,
            user_id = user_id,
            schedules_common_id = schedules_common_id
          )
          db.session.add(new_schedules_date)
          db.session.commit()
          currdate = currdate + datetime.timedelta(days=cycle)

        #response는 medicine_id와 schedules_common_id
        results = {
          'medicine_id': medicine_id,
          'schedules_common_id': schedules_common_id
        }

        response_object = {
          'status': 'OK',
          'message': 'Successfully post schedules date.',
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

def edit_schedules_date(data):
  """ Post Schedules Date API"""
  try:
    cycle = data['cycle']
    schedules_common_id = data['schedules_common_id']
    time = data['time']

    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      if decoded_token:
        data = db.session.query(Schedules_common.startdate, Schedules_common.enddate, Schedules_common.cycle).filter(and_(Schedules_common.id==schedules_common_id, Schedules_common.user_id==user_id)).all() 
        startdate = datetime.datetime.strptime(data[0].startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(data[0].enddate, '%Y-%m-%d')
        cycle = data[0].cycle #2
        print(startdate, enddate, cycle)
        #여기까지 post와 동일
        
        currdate = now.strftime('%Y-%m-%d %H:%M:%S') #오늘자 기준으로 for loop 돌리기
        # 1. 우선 DB내에서 오늘이후의 schedules_date 지우기
        while currdate <=enddate:
          saved_schedule = Schedules_date.query.filter_by(alarmdate=currdate).first()
          db.session.delete(saved_schedule)
          db.session.commit()
          currdate = currdate + datetime.timedelta(days=cycle)

        
        # while currdate <= enddate:
        #   #이를 schedules_date 테이블에 넣어주기
        #   new_schedules_date = Schedules_date(
        #     alarmdate = currdate,
        #     time = time,
        #     check = 0,
        #     user_id = user_id,
        #     schedules_common_id = schedules_common_id
        #   )
        #   db.session.add(new_schedules_date)
        #   db.session.commit()
        #   currdate = currdate + datetime.timedelta(days=cycle)

        # #response는 medicine_id와 schedules_common_id
        # results = {
        #   'medicine_id': medicine_id,
        #   'schedules_common_id': schedules_common_id
        # }

        # response_object = {
        #   'status': 'OK',
        #   'message': 'Successfully post schedules date.',
        #   'results': results
        # }
        # return response_object, 200

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