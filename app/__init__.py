from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as users_ns
from .main.controller.post_controller import api as posts_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus (restx) web service'
          )

api.add_namespace(users_ns, path='/user')
api.add_namespace(posts_ns)