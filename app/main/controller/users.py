from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.users import get_find_id

api = UserDto.api

@api.route('/email')
class GetFindID(Resource):
  def post(self):
    """Get Find ID"""
    data = request.args.to_dict('users')
    return get_find_id(data)
