#-*- coding: utf-8 -*-
# users 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_ 
import json
import jwt
from flask_bcrypt import bcrypt
from app.main import db
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg 


def post_login(data):
  """Post Login"""
  try:
    try:
      email = data['email']
      password = data['password'] 
      pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) 

      user = Users.query.filter(and_(Users.email==email, Users.password==pw_hash)).first()
      if user:
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
          'message': 'Unvalid User.',
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