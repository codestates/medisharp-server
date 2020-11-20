from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
    })


class PostDto:
    api = Namespace('post', description='post related operations')
    post = api.model('postt_details', {
        'title': fields.String(required=True, description='The post title'),
        'content': fields.String(required=True, description='The post content '),
    })
