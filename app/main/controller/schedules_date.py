from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_dateDto
import requests, jwt
from ..service.schedules_date import get_monthly_checked, get_alarms_list, get_today_checked, patch_check
from app.main import db
from ..config import jwt_key, jwt_alg

api = Schedules_dateDto.api
_schedules_date = Schedules_dateDto.schedules_date


def response_ok(result):
  response_object = { 
    'status': 'OK', 
    'message': 'Successfully get today checked.',
    'results': result
  }
  return response_object

def response_err():
  response_object = {
    'status': 'Internal Server Error',
    'message': 'Some Internal Server Error occurred.',
  }
  return response_object


@api.route('/check')
class PatchCheck(Resource):
  def patch(self):
    """Patch Check API"""
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
      if user_id:
        data = request.get_json().get('schedules_common') 
        result = patch_check(data, user_id)
        db.session.commit()
        return response_ok(result), 200
    except Exception as e:
      db.session.rollback()
      raise
      return response_err(), 500
    finally:
      db.session.close()


@api.route('/check/month') 
class Check(Resource):
  def get(self):
    """Get Montly Checked API"""
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']   
      if user_id: 
        params = request.args.to_dict()
        result =  get_monthly_checked(params, user_id)
        return response_ok(result), 200
    except Exception as e:
      return response_err(), 500


@api.route('/schedules-commons/alarm')
class TodayAlarmList(Resource):
  def get(self):
    """Get Alarms List on Clicked date"""
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
      if user_id:
        params = request.args.to_dict()
        result = get_alarms_list(params, user_id)
        return response_ok(result), 200
    except Exception as e:
      return response_err(), 500
  

@api.route('/today') 
class Check(Resource):
  def get(self):
    """Get Today Alarm API"""
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
      if user_id:
        params = request.args.to_dict()
        result = {'today_check' : get_today_checked(params, user_id) , 'today_alarm' : get_alarms_list(params, user_id)}
        return response_ok(result), 200
    except Exception as e:
      return response_err(), 500
      



