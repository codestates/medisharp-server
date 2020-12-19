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


def delete_user_info(data):
  """Delete User Info API"""
  try:
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token, jwt_key, jwt_alg)
    user_id = decoded_token['id']
    if decoded_token:
      session.clear()

      response_object = {
        'status': 'OK',
        'message': 'Successfully Delete User Info.',
      }
      return response_object, 200

  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500 
