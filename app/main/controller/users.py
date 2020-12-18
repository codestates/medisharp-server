from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.users import post_signup

api = UserDto.api

# @api.route('/login')
# class PostLogin(Resource):
#   def post(self):
#     """Post Login"""
#     data = request.get_json().get('users')
#     return post_login(data)

@api.route('/signup')
class PostSignup(Resource):
  def post(self):
    """Post Signup"""
    data = request.get_json().get('users')
    return post_signup(data)
