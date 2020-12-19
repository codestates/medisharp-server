#데이터를 http로 처리할 controller를 만들어 주겠습니다. 그러면서 util 폴더와 한번 소통합니다. 
#이는 해당 api 가 어느 DB와 소통하는지 한번 점검 해주는 느낌이라고 보시면 될거 같아요!
#여기선 실제로 DB에서 데이터를 주고받는 과정 직전까지의 코드를 짜줍니다


from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.users import social_signin
from ..config import kakao_client_id

api = UserDto.api

@api.route("/oauth/kakao") 
class KakaoSignIn(Resource):
    def get(self):
        client_id = kakao_client_id
        redirect_uri = "http://127.0.0.1:5000/users/oauth/kakao/callback"
        kakao_oauthurl = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(kakao_oauthurl)


@api.route("/oauth/kakao/callback") 
class KakaoSignInCallback(Resource):
    def get(self):
        #print("request.GET :" , request.args.get)
        try:
            code = request.args.get("code")                                 
            client_id = kakao_client_id
            redirect_uri = "http://127.0.0.1:5000/users/oauth/kakao/callback"
            
            token_request = requests.get(                                       
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )
            
            token_json = token_request.json() 

            error = token_json.get("error",None)

            if error is not None :
                return make_response({"message": "INVALID_CODE"}, 400) 

            access_token = token_json.get("access_token") 
            #print("access_token:", access_token)                       

            profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
                )
            data = profile_request.json()
            # 위의 코드로 이번엔 카카오에서 유저 정보를 담은 url에 access token을 담아서, 유저 정보를 겟 요청합니다.

        except KeyError:
            return make_response({"message" : "INVALID_TOKEN"}, 400)

        except access_token.DoesNotExist:
            return make_response({"message" : "INVALID_TOKEN"}, 400)
          
        return social_signin(data=data) # 이젠 위에서 받은 데이터를 DB에 넣어줘야 합니다. 이 과정이 service에서 진행됩니다.
