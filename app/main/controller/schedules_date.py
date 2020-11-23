from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_dateDto
import requests
from ..service.schedules_date import get_monthly_checked

api = Schedules_dateDto.api
_schedules_date = Schedules_dateDto.schedules_date

@api.route('/check/month') 
class Check(Resource):
 
  def get(self):
    """Get Montly Checked API"""

    data = request.args.to_dict()
    return get_monthly_checked(data)