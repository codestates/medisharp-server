#-*- coding: utf-8 -*-
# medicines 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_
import json
import jwt
from datetime import time
from operator import itemgetter
from app.main import db
from app.main.model.medicines import Medicines
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg

def post_medicine(data):
  """ Gost medicine information"""
  try:
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token, jwt_key, jwt_alg)
    user_id = decoded_token['id']
    if decoded_token:
      for el in data:
        new_medicine = Medicines(
          name=el['name'], 
          title=el['title'],
          image_dir=el['image_dir'],
          effect=el['effect'],
          capacity=el['capacity'],
          validity=el['validity'],
          camera=el['camera']
          )
        print('new_medicine: ', new_medicine)
        db.session.add(new_medicine)
      db.session.commit()
      response_object = {
        'status': 'OK',
        'message': 'Successfully get monthly checked.',
      }
      return response_object, 200
    else:
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