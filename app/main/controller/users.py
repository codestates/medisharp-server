from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.users import get_find_user

api = UserDto.api

@api.route('/id')
class GetFindUser(Resource):
  def get(self):
    """Post Login"""
    data = request.args.to_dict()
    return get_find_user(data)