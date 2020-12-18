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


def post_logout(data):
  """Post Logout"""
  try:
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
   
      if decoded_token:
        session.pop('email', None)
        return redirect('/')
            
        response_object = {
          'status': 'OK',
          'message': 'Successfully post logout.',
        }
        return response_object, 200
    except Exception as e:
      print(e)
      response_object = {
        'status': 'fail',
        'message': 'You Are Currently Not Logined.',
      }
      return response_object, 400

  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500