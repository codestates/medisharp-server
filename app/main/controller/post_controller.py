from flask import request
from flask_restx import Resource

from ..util.dto import PostDto

api = PostDto.api
_post = PostDto.post

# @api.route('/login')
# class UserLogin(Resource):
#     """
#         User Login Resource
#     """
#     @api.doc('user login')
#     @api.expect(user_auth, validate=True)
#     def post(self):
#         # get the post data
#         post_data = request.json
#         return Auth.login_user(data=post_data)


# @api.route('/logout')
# class LogoutAPI(Resource):
#     """
#     Logout Resource
#     """
#     @api.doc('logout a user')
#     def post(self):
#         # get auth token
#         auth_header = request.headers.get('Authorization')
#         return Auth.logout_user(data=auth_header)