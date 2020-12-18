from flask_restx import Api
from flask import Blueprint

from .main.controller.schedules_common import api as schedules_common
from .main.controller.schedules_date import api as schedules_date
from .main.controller.medicines import api as medicines
from .main.controller.oauth import api as oauth 
from .main.controller.test import api as test
from .main.controller.users import api as users

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus (restx) web service'
          )

api.add_namespace(schedules_common, path='/schedules-commons')
api.add_namespace(schedules_date, path='/schedules-dates')
api.add_namespace(medicines, path='/medicines')
#api.add_namespace(oauth, path="/oauth/kakao") 
api.add_namespace(users, path="/users")
api.add_namespace(test)
