from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_dateDto
import requests
from ..service.schedules_date import get_monthly_checked, get_alarms_list, get_today_checked

api = Schedules_dateDto.api
_schedules_date = Schedules_dateDto.schedules_date

@api.route('/check/month') 
class Check(Resource):
 
  def get(self):
    """Get Montly Checked API"""
    data = request.args.to_dict()
    return get_monthly_checked(data)


@api.route('/schedules-commons/alarm/today')
class TodayAlarmList(Resource):
  def get(self):
    """Get Alarms List on Clicked date"""
    data = request.args.to_dict()
    return get_alarms_list(data)
  

@api.route('/check/today') 
class Check(Resource):
 
  def get(self):
    """Get Today Checked API"""
    data = request.args.to_dict()
    return get_today_checked(data)

