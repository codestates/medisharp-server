#데이터를 http로 처리할 controller를 만들어 주겠습니다.


from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.oauth import social_signin

api = UserDto.api
_user = UserDto.user

@api.route("/")
class KakaoSignIn(Resource):
    def get(self):
        client_id = "337ef29844da6a8441a6d6758461107b"
        redirect_uri = "http://127.0.0.1:5000/oauth/kakao/callback"
        kakao_oauthurl = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(kakao_oauthurl)


@api.route("/callback")
class KakaoSignInCallback(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        print("request.GET :" , request.args.get)
        try:
            code = request.args.get("code")                                       
            client_id = "337ef29844da6a8441a6d6758461107b"
            redirect_uri = "http://127.0.0.1:5000/oauth/kakao/callback"
            
            print("code :" , code)

            #Python에서 HTTP 요청을 보내는 모듈인 requests
            #1차적으로 redirect uri를 통해서 request token을 카카오로부터 받아온다. 그것이 code이다
            token_request = requests.get(                                       
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )
            
            token_json = token_request.json()  

            print("token_json:", token_json)                                
            

            error = token_json.get("error",None)

            if error is not None :
                return make_response({"message": "INVALID_CODE"}, 400)

            access_token = token_json.get("access_token")  
            print("access_token:", access_token)                       

            profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
                )
            profile_json = profile_request.json()
            print("profile_json:", profile_json)

            kakao_account = profile_json.get("properties")
            email = kakao_account.get("nickname", None)
            kakao_id = profile_json.get("id")

            print("kakao_account:", kakao_account)
            print("email:", email)
            print("kakao_id:", kakao_id)

        except KeyError:
            return make_response({"message" : "INVALID_TOKEN"}, 400)

        except access_token.DoesNotExist:
            return make_response({"message" : "INVALID_TOKEN"}, 400)
          
        return social_signin()
