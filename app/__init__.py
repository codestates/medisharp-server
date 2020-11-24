# from flask_restx import Api
# from flask import Blueprint

# #from .main.controller.user_controller import api as users_ns
# #from .main.controller.post_controller import api as posts_ns

# blueprint = Blueprint('api', __name__)

# api = Api(blueprint,
#           title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
#           version='1.0',
#           description='a boilerplate for flask restplus (restx) web service'
#           )

# api.add_namespace(users_ns, path='/user')
# api.add_namespace(posts_ns) 

from flask_restx import Api
from flask import Blueprint

# blueprint = Blueprint('api', __name__)
from .main.controller.oauth import api as oauth 
#controller의 oauth가 DB와 소통하기 위해 util 파일과 연결되어있는 api 함수를 불러옵니다. 불러오되 이름을 as oauth로 지정해줍니다.
from .main.controller.test import api as test

# api = Api(blueprint,
#           title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
#           version='1.0',
#           description='a boilerplate for flask restplus (restx) web service'
#           )
blueprint = Blueprint('api', __name__)

# api.add_namespace(users_ns, path='/user')
# api.add_namespace(posts_ns)  
api = Api(blueprint,
          title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus (restx) web service'
          )

api.add_namespace(oauth, path="/oauth/kakao") #이 라우팅을 따라서 우선 controller의 oauth로 갑니다
api.add_namespace(test) #이건 제가 테스트용으로 추가한건데 참고하시면 좋을거 같아서 그대로 뒀어요 