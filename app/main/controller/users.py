from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.users import delete_user_info

api = UserDto.api

@api.route('/signout')
class DeleteUserInfo(Resource):
  def delete(self):
    """Delete User Info"""
    data = request.args.to_dict()
    return delete_user_info(data)