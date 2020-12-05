from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import MedicinesDto
import requests
from ..service.medicines import post_schedules_common_medicines

api = MedicinesDto.api
#_medicines = MedicinesDto.medicines


@api.route('/schedules-medicines') 
class PostSchedulesCommonMedicines(Resource):
  def post(self):
    """Post Schedules Common Medicines API"""
    data = request.get_json().get('schedules_common_medicines') 
    return post_schedules_common_medicines(data) 
