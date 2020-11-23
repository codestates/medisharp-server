from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_dateDto
import requests
from ..service.schedules_date import get_monthly_checked

api = Schedules_dateDto.api
_schedules_date = Schedules_dateDto.schedules_date

#query parameter는 이렇게 쓰는게 아니라 check아래에서 분기하는 형태로 구현해줘야 할 거 같다. 일단 이렇게 쓰고.. 나중에 꼭 고칠 것!
# @api.route('/check?during=month') #parameter를 이렇게 하는게 아니었다! 이것때문에 에러가 발생한 것이었다!!
@api.route('/check/month') 
class Check(Resource):
 
  def get(self):
    """Get Montly Checked API"""
    print("Get Monthly Checked API request .GET: ", request.args.get) #[]
    data = request.args.to_dict()
    print(data)


    return get_monthly_checked(data)