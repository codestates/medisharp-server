from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import Schedules_medicinesDto
import requests
from ..service.schedules_medicines import post_schedules_medicines

api = Schedules_medicinesDto.api
_schedules_medicines = Schedules_medicinesDto.schedules_medicines


@api.route('') 
class PostSchedulesCommonMedicines(Resource):
  def post(self):
    """Post Schedules Common Medicines API"""
    data = request.get_json().get('schedules_common_medicines') 
    return post_schedules_common_medicines(data) 
