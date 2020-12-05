from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_commonDto
import requests
from ..service.schedules_common import post_schedules_common

api = Schedules_commonDto.api
_schedules_common = Schedules_commonDto.schedules_common


@api.route('') 
class PostSchedulesCommon(Resource):
  def post(self):
    """Post Schedules Common API"""
    data = request.get_json().get('schedules_common') 
    return post_schedules_common(data) 

@api.route('/schedules-date') 
class PostSchedulesDate(Resource):
  def post(self):
    """Post Schedules Date API"""
    data = request.get_json().get('schedules_common') 
    return post_schedules_common(data) 