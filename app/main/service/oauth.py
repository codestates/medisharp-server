from flask import request, redirect
import jwt

from app.main import db
from app.main.model.users import Users

from ..config import jwt_key, jwt_alg



def social_signin(data):
    #print("profile_json:", data)

    kakao_account = data.get("properties")
    email = kakao_account.get("nickname", None)
    kakao_id = str(data.get("id"))

    #print("kakao_account:", kakao_account)
    #print("email:", email)
    #print("kakao_id:", kakao_id)
    user = Users.query.filter_by(email=email).first()
    if not user:
      new_user = Users(
            email=email,
            password=kakao_id,
            full_name=email,
            mobile='null',
            login='social'
      )
      save_social(new_user)
      token = jwt.encode({"email":email}, jwt_key, jwt_alg)
      token = token.decode("utf-8")
      print("token:", token)
      response_object = {
          'status': 'success',
          'message': '회원가입 되었습니다.'
      }
      return response_object, token, 200
    else:
      print("user:", user.email)
      email = user.email
      token = jwt.encode({"email":email}, jwt_key, jwt_alg)
      token = token.decode("utf-8")
      print("token:", token)
      response_object = {
          'status': 'already signin',
          'message': '이미 가입된 회원입니다.',
      }
      return response_object, 201


def save_social(data):
    db.session.add(data)
    db.session.commit()