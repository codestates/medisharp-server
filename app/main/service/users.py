#-*- coding: utf-8 -*-
# users 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_ , create_engine
import json ,io
from sqlalchemy.sql import text
import jwt
from app.main import db
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg , get_s3_connection, S3_BUCKET, S3_REGION, DevelopmentConfig #배포때는 여기를 ProductionConfig로 해주어야 합니다. 


def post_login(data):
  """Post Login"""
  try:
    try:
      email = data['email']
      password = data['password']  
      
      if (email in Users and password in Users):
        token = jwt.encode({"id":new_user.id}, jwt_key, jwt_alg) 
        token = token.decode("utf-8")     
            
        response_object = {
          'status': 'OK',
          'message': 'Successfully post login.',
          'Authorization': token
        }
        return response_object, 200
    except Exception as e:
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