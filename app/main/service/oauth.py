from flask import request, redirect
import jwt

from app.main import db
from app.main.model.users import Users

from ..config import jwt_key, jwt_alg



def social_signin(data):
    #print("profile_json:", data)
    # 받아온 데이터에서 쓸만한건 유저 닉네임이랑 id 정도더라구요.
    # 닉네임을 이메일처럼/ id를 비번처럼 활용하면 어떨까 했습니다.

    kakao_account = data.get("properties")
    email = kakao_account.get("nickname", None)
    kakao_id = str(data.get("id")) # 모델에서 비번을 str으로 설정했기 때문에 여기서 문자열로 변경안해주면 에러가!

    #print("kakao_account:", kakao_account)
    #print("email:", email)
    #print("kakao_id:", kakao_id)
    user = Users.query.filter_by(email=email).first() # 이메일값으로 쿼리 필터를 한번 해주고
    if not user: # 없으면 데이터를 생성합니다
      new_user = Users(
            email=email,
            password=kakao_id,
            full_name=email,
            mobile='null',
            login='social'
      )
      save_social(new_user) # 아래에 정의된 함수입니다. DB에 위에 정의한 데이터를 저장!
      print("user:", new_user.id)
      token = jwt.encode({"id":new_user.id}, jwt_key, jwt_alg) #그리고 저장했으니 토큰을 만들어줘야겠죠
      token = token.decode("utf-8")
      print("token:", token)
      response_object = {
          'status': 'success',
          'message': '회원가입 되었습니다.',
          'Authorization': token
      }
      return response_object, 200 # 위에서 만든 토큰을 클라에서 보냅니다
    else: # 이건 로그인 시도했는데 데이터가 있는 경우
      user_id = user.id 
      print("user:", user_id)
      token = jwt.encode({"id":user_id}, jwt_key, jwt_alg) #토큰을 만들어줍니다
      token = token.decode("utf-8")
      #print("token:", token)
      response_object = {
          'status': 'already signin',
          'message': '이미 가입된 회원입니다.',
          'Authorization': token
      }
      return response_object, 201


def save_social(data):
    db.session.add(data)
    db.session.commit()