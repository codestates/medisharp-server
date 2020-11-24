#데이터를 http로 처리할 controller를 만들어 주겠습니다. 그러면서 util 폴더와 한번 소통합니다. 
#이는 해당 api 가 어느 DB와 소통하는지 한번 점검 해주는 느낌이라고 보시면 될거 같아요!
#여기선 실제로 DB에서 데이터를 주고받는 과정 직전까지의 코드를 짜줍니다


from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import UserDto
import requests
from ..service.oauth import social_signin

api = UserDto.api

@api.route("/") # 카카오 로그인하기를 누르면 우선 해당 api로 오게되고, redirect를 통해 바로 request token을 받기 위해 링크가 변경됩니다.
class KakaoSignIn(Resource):
    def get(self):
        client_id = "337ef29844da6a8441a6d6758461107b"
        redirect_uri = "http://127.0.0.1:5000/oauth/kakao/callback"
        kakao_oauthurl = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(kakao_oauthurl)


@api.route("/callback") # 위의 라우팅에서 redirect 되면서 바로 이 api로 오게됩니다.
class KakaoSignInCallback(Resource):
    def get(self):
        #print("request.GET :" , request.args.get)
        try:
            code = request.args.get("code")  # callback 뒤에 붙어오는 request token을 뽑아내 줍니다.                                    
            client_id = "337ef29844da6a8441a6d6758461107b"
            redirect_uri = "http://127.0.0.1:5000/oauth/kakao/callback"
            
            #print("code :" , code)

            #Python에서 HTTP 요청을 보내는 모듈인 requests
            #node보다 장점을 드디어 찾았어요!
            #node에선 서버를 클라화 해주기 위해 아씨오를 부르고 이래저래 했는데, flask에서는 requests 라는 모듈을 써서 바로 해당 url로 get 요청을 보낼수있어요
            token_request = requests.get(                                       
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )
            
            token_json = token_request.json()  # 위의 get 요청을 통해 받아온 데이터를 json화 해주면 이곳에 access token 이 숨어있습니다.

            #print("token_json:", token_json)                                
            

            error = token_json.get("error",None)

            if error is not None :
                return make_response({"message": "INVALID_CODE"}, 400) #에러 처리 한번 해주고

            access_token = token_json.get("access_token") #카카오 소셜로그인을 통해 유저에 대한 정보를 받을 권한이 있는 토큰이 이것입니다. 
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
