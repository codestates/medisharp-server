from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_commonDto
import requests
from ..service.schedules_common import post_schedules_common

api = Schedules_commonDto.api
_schedules_common = Schedules_commonDto.schedules_common

<<<<<<< HEAD

=======
"""
client에서 body에 
{
  "schedules_common": 
    {"title": "처방받은 수면제", 
      "memo": "자기전에 꼭 먹어",
      "startdate": 6,
      "enddate": 20,
      "cycle": 2,
      "time": 22:00:00,(이건 schedules_date에 넘겨주어야 할 정보)
    }, 
}
의 형태로 온다고 생각하고 구현
"""
>>>>>>> Dev
@api.route('') 
class PostSchedulesCommon(Resource):
  def post(self):
    """Post Schedules Common API"""
    data = request.get_json().get('schedules_common') 
<<<<<<< HEAD
    return post_schedules_common(data) 

@api.route('/schedules-dates') 
class PostSchedulesDate(Resource):
  def post(self):
    """Post Schedules Date API"""
    results = request.get_json().get('schedules_common') 
    return post_schedules_common(data) 
=======
    return post_schedules_common(data)
>>>>>>> Dev
