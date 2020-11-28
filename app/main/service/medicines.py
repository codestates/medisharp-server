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

"""
클라에서 Request로 주는 약 정보
medicine: [
  {"name": "타이레놀", 
    "title": "머리 아플 때 먹어",
    "image_dir": "https://s3.amazonaws.com/bucketname/foldername/image1.jpg",
    "effect": "두통",
    "capacity": "성인2알",
    "validity": "개봉 후 2년",
    "camera": false
  }, 
   {"name": "이가탄", 
    "title": "이 아플 때 먹어",
    "image_dir": "https://s3.amazonaws.com/bucketname/foldername/image2.jpg",
    "effect": "치통",
    "capacity": "성인1알",
    "validity": "개봉 후 2년",
    "camera": true
  },
]
라고 생각하고 구현
"""

def post_medicine(data):
  """ Gost medicine information"""
  try:
    # token = request.headers.get('Authorization')
    # decoded_token = jwt.decode(token, jwt_key, jwt_alg)
    # user_id = decoded_token['id']

    # if decoded_token:
    print("data is", data)
    user_id = 1
    if user_id: 
      new_medicine = Medicines(
        name=data['name'], 
        title=data['title'],
        image_dir=data['image_dir'],
        effect=data['effect'],
        capacity=data['capacity'],
        validity=data['validity'],
        camera=data['camera']
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








