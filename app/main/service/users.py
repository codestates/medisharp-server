#-*- coding: utf-8 -*-
# users 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_ , create_engine
import json ,io
from sqlalchemy.sql import text
import jwt
import bcrypt
from app.main import db
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg , get_s3_connection, S3_BUCKET, S3_REGION, DevelopmentConfig #배포때는 여기를 ProductionConfig로 해주어야 합니다. 


# def post_login(data):
#   """Post Login"""
#   try:
#     try:
#       email = data['email']
#       password = data['password']  
#       password = bycrypt.checkpw(password.encode("utf-8")

#       user = Users.query.filter_by(email=email, password=password).first()
#       if user:
#         token = jwt.encode({"id": user.id}, jwt_key, jwt_alg) 
#         token = token.decode("utf-8")     

#         response_object = {
#           'status': 'OK',
#           'message': 'Successfully post login.',
#           'Authorization': token
#         }
#         return response_object, 200
#     except Exception as e:
#       print(e)
#       response_object = {
#         'status': 'fail',
#         'message': 'Unvalid User.',
#       }
#       return response_object, 401

#   except Exception as e:
#       response_object = {
#         'status': 'Internal Server Error',
#         'message': 'Some Internal Server Error occurred.',
#       }
#       return response_object, 500 


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

      if user is None:
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


def get_find_id(data):
  """Get Find ID API"""
  try:
    print(data)
    try:
      full_name = data['full_name']
      mobile = data['mobile']
      mobile = bycrypt.checkpw(mobile.encode("utf-8"))
      
      user = Users.query.filter_by(full_name=full_name, mobile=mobile).first()

      if user:
        email = db.session.query(Users.email).filter(and_(Users.full_name==full_name, Users.mobile==mobile)).all() 

        response_object = {
          'status': 'OK',
          'message': 'Successfully Get Find ID.',
          'email': email
        }
        return response_object, 200
    except Exception as e:
      print(e)
      response_object = {
        'status': 'fail',
        'message': '일치하는 회원 정보가 없습니다. 회원가입 혹은 소셜로그인을 시도해보세요.',
      }
      return response_object, 404

  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500 