#-*- coding: utf-8 -*-
#schedules_medicines 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_
import json
import jwt
import re
from datetime import time
from operator import itemgetter
from app.main import db
from app.main.model.schedules_date import Schedules_date
from app.main.model.schedules_common import Schedules_common
from app.main.model.medicines import Medicines
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg


def post_schedules_common_medicines(data): 
  """ Post Schedules Common Medicines API """
  try:
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token, jwt_key, jwt_alg)
    user_id = decoded_token['id']

    if decoded_token:
      new_id = schedules_medicines(
        medicines_id=medicines_id,
        schedules_common_id=schedules_common_id,
      )        
      new_id.schedules_medicines.append()
      db.session.add(new_id)
      db.session.commit()

      results = {
        "new_schedules_medicines_id": new_id.id
      }

      response_object = {
        'status': 'OK',
        'message': 'Successfully Post Schedules Common Medicines.',
        'results': results
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