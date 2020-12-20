from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_ , create_engine
import json ,io
from sqlalchemy.sql import text
import jwt
import bcrypt
from app.main import db
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg , DevelopmentConfig #배포때는 여기를 ProductionConfig로 해주어야 합니다. 


def post_signup(data):
  """Post Login"""
  try:
    try:
      full_name = data['full_name']
      email = data['email']
      password = data['password']  
      mobile = data['mobile']
      login = 'basic'

      user = Users.query.filter_by(email=data['email']).first()

      if user == None:
        new_user = Users(
          full_name = data['full_name'],
          email = data['email'],
          password = data['password'], 
          mobile = data['mobile'],
          login = 'basic'
        )
        db.session.add(new_user)
        db.session.commit()

        response_object = {
          'status': 'OK',
          'message': 'Successfully Post Signup.',
        }
        return response_object, 200
      except Exception as e:
        print(e)
        response_object = {
          'status': 'fail',
          'message': 'Already a Registered User.',
        }
        return response_object, 409
     except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500


def post_login(data):
  """Post Login"""
  try:
    try:
      email = data['email']
      password = data['password'] 

      user = Users.query.filter_by(email=email).first()
      if user:
        if flask_bcrypt.check_password_hash(user.password, password):
          token = jwt.encode({"id": user.id}, jwt_key, jwt_alg) 
          token = token.decode("utf-8")     

          response_object = {
            'status': 'OK',
            'message': 'Successfully post login.',
            'Authorization': token
          }
          return response_object, 200
        else:
          response_object = {
          'status': 'fail',
          'message': 'Unvalid user password.',
          }
          return response_object, 401
      else:
        response_object = {
          'status': 'fail',
          'message': 'Unvalid user email.',
        }
        return response_object, 401
    except Exception as e:
      print(e)
      response_object = {
        'status': 'fail',
        'message': 'Unvalid User.',
      }
      return response_object, 401
  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500 

def social_signin(data):
    #print("profile_json:", data)
    # 받아온 데이터에서 쓸만한건 유저 닉네임이랑 id 정도더라구요.
    # 닉네임을 이메일처럼/ id를 비번처럼 활용하면 어떨까 했습니다.
    try:
      kakao_account = data.get("properties")
      email = kakao_account.get("nickname", None)
      kakao_id = str(data.get("id")) # 모델에서 비번을 str으로 설정했기 때문에 여기서 문자열로 변경안해주면 에러가!
      try:
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
          db.session.add(new_user)
          db.session.commit()
          print("user:", new_user.id)
          token = jwt.encode({"id":new_user.id}, jwt_key, jwt_alg) #그리고 저장했으니 토큰을 만들어줘야겠죠
          token = token.decode("utf-8")
          print("token:", token)
          response_object = {
              'status': 'success',
              'message': 'you become a member for our service',
              'Authorization': token
          }
          return response_object, 200 
        else: 
          user_id = user.id 
          print("user:", user_id)
          token = jwt.encode({"id":user_id}, jwt_key, jwt_alg) 
          token = token.decode("utf-8")
          #print("token:", token)
          response_object = {
              'status': 'already signin',
              'message': 'you already our member. login success',
              'Authorization': token
          }
          return response_object, 201
      except Exception as e:
        db.session.rollback()
        print(e)
        response_object = {
          'status': 'fail',
          'message': 'Provide a valid auth token.',
        }
        return response_object, 401
    except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500 


