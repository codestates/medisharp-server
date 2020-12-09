from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_commonDto
import requests
from ..service.schedules_common import post_schedules_common, post_schedules_date , get_schedules_common

api = Schedules_commonDto.api
_schedules_common = Schedules_commonDto.schedules_common

@api.route('') 
class PostSchedulesCommon(Resource):
  def get(self):
    """Get Schedules Common API"""
    data = request.args.to_dict()
    print(data)
    return get_schedules_common(data)

  def post(self):
    """Post Schedules Common API"""
    data = request.get_json().get('schedules_common') 
    return post_schedules_common(data) 

  


"""
client에서 
{
  "schedules_common":
    {
      "medicine_id": [1, 2, 3],
      "schedules_common_id": 1, 
      "time": 11:30:00
    }
}
을 request에 준다고 가정하고 짠다. 
"""


@api.route('/schedules-dates') 
class PostSchedulesDate(Resource):
  def post(self):
    """Post Schedules Date API"""
    data = request.get_json().get('schedules_common') 
    return post_schedules_date(data) 

