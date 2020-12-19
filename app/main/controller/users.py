from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.users import post_login

api = UserDto.api

@api.route('/login')
class PostLogin(Resource):
  def post(self):
    """Post Login"""
    data = request.get_json().get('users')
    return post_login(data)