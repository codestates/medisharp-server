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

def edit_schedules_common(data):
  """ Edit Common information of alarm"""
  try:
    schedules_common_id = data['schedules_common_id']
    try: 
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
      if decoded_token:
        # 1. 전체 데이터 넘어오고 서버에서 변경된 것만 update 해주는 경우
        #우선 저장되어있는 데이터 select 해오기
        topic_fields = {
          'title' : fields.String(required=True),
          'startdate': fields.String(required=True),
          'enddate': fields.String(required=True),
          'cycle': fields.Integer(required=True),
          'memo': fields.String(required=True),
        }
        saved_schedule = [marshal(topic, topic_fields) for topic in Schedules_common.query.filter(and_(Schedules_common.id==schedules_common_id, Schedules_common.user_id==user_id)).all()]
        print(saved_schedule[0])
        # 전달받아온 데이터를 for 문을 돌면서, 해당 DB에서 대조하지 않아도 되는 키값은 제외하고, 각 value 비교해서 달라진 경우만 update
        for key in data.keys():
          if not key == "schedules_common_id" and not key == "time":
            if not data[key] == saved_schedule[0][key]:
              schedules_common = Schedules_common.query.filter_by(id =schedules_common_id).update({key: data[key]})
              db.session.commit()
        
        # 2. client에서 변경된 데이터만 전달해줄 수 있는 경우
        # for key in data.keys():
        #   if not key == "schedules_common_id" and not key == "time":
        #     schedules_common = Schedules_common.query.filter_by(id =schedules_common_id).update({key: data[key]})
        #     db.session.commit()
        results = {
          "time": data['time']
        }

        response_object = {
          'status': 'OK',
          'message': 'Successfully Edit Common information of alarm.',
          'results' : results,
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


