from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_dateDto
import requests
from ..service.schedules_date import get_monthly_checked, get_alarms_list, get_today_checked, patch_check
from app.main import db

api = Schedules_dateDto.api
_schedules_date = Schedules_dateDto.schedules_date

@api.route('/check')
class PatchCheck(Resource):
  def patch(self):
    """Patch Check API"""
    data = request.get_json().get('schedules_common') 
    return patch_check(data)

@api.route('/check/month') 
class Check(Resource):
  def get(self):
    """Get Montly Checked API"""
    data = request.args.to_dict()
    return get_monthly_checked(data)


@api.route('/schedules-commons/alarm')
class TodayAlarmList(Resource):
  def get(self):
    """Get Alarms List on Clicked date"""
    data = request.args.to_dict()
    return get_alarms_list(data)
  

@api.route('/today') 
class Check(Resource):
  def get(self):
    """Get Today Alarm API"""
    try:
      req = request.args.to_dict()
      result = {'today_check' : get_today_checked(req) , 'today_alarm' : get_alarms_list(req)}
      print(result)
      response_object = { 
          'status': 'OK', 
          'message': 'Successfully get today checked.',
          'results': result
        }
      return response_object, 200
    except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500
      



