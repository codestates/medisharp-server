#dto는 data transfer object로 데이터를 전달하는 기능을 합니다.
from flask_restx import Namespace, fields


#User 데이터를 전달하는 함수를 만들어 줍니다.
class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'full_name': fields.String(description='user full_name'),
        'password': fields.String(required=True, description='user password'),
        'mobile': fields.String(description='user mobile num'),
        'login': fields.String(required=True, description='user kind login')
    })