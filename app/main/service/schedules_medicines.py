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
from app.main.model.medicines import medicines
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg


def post_schedules_common_medicines(data): 
  """ Post Schedules Common Medicines API """

    if data:
      Schedules_medicines = schedules_medicines(
        schedules_common_id,
        medicines_id
      }
     db.session.add(Schedules_medicines)
     db.session.commit()

      response_object = {
        'status': 'OK',
        'message': 'Successfully Post Schedules Common Medicines.',
      }
      return response_object, 200
      
    else:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500
