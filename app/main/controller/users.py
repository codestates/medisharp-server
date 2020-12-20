from flask import request, redirect, jsonify, make_response
from flask_restx import Resource
from ..util.dto import UserDto
import requests
from ..service.users import post_login, social_signin
from ..config import kakao_client_id

api = UserDto.api

@api.route('/login')
class PostLogin(Resource):
  def post(self):
    """Post Login"""
    data = request.get_json().get('users')
    return post_login(data)


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

