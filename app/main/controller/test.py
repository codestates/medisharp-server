from flask import request, redirect
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.test import get_all_users


api = UserDto.api
_user = UserDto.user

@api.route('/')
class test(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        return get_all_users()