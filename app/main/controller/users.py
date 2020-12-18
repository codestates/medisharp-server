from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.users import post_logout

api = UserDto.api

@api.route('/logout')
class PostLogout(Resource):
  def post(self):
    """Post Logout"""
    data = request.get_json().get('users')
    return post_logout(data)