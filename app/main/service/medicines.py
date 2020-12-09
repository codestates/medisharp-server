#-*- coding: utf-8 -*-
# medicines 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_
from PIL import Image
import json ,io
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import jwt
from datetime import time
from operator import itemgetter
from app.main import db
from app.main.model.medicines import Medicines
from app.main.model.users import Users
import requests, bs4
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import pandas as pd
from ..config import jwt_key, jwt_alg , get_s3_connection, S3_BUCKET, S3_REGION, DevelopmentConfig #배포때는 여기를 ProductionConfig로 해주어야 합니다. 


def post_medicine(data):
  """Post medicine information"""
  try:
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      if decoded_token:
        medicine_ids = []
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
          db.session.add(new_medicine)
          db.session.commit()
          medicine_ids.append(new_medicine.id)

        response_object = {
          'status': 'OK',
          'message': 'Successfully post medicine information.',
          'medicine_id': medicine_ids
        }
        return response_object, 200
    except Exception as e:
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


def post_schedules_common_medicines(data):
  """Post schedules_common_id | medicines_id in schedules_medicines table 
  Because that model exists, I wrote the query statement directly, not the ORM syntax.
  reference: https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/
  """
  try:
    schedules_common_id = data['schedules_common_id']
    medicines_id = data['medicines_id']
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI) #배포때는 여기를 ProductionConfig.SQLALCHEMY_DATABASE_URI 로 해주어야 합니다. 
      query = text("""INSERT INTO schedules_medicines(schedules_common_id, medicines_id) VALUES (:each_schedules_common_id, :each_medicine_id)""")
      each_schedules_common_id = schedules_common_id
      with engine.connect() as con:
        for each_medicine_id in medicines_id:
          new_schedules_medicine = con.execute(query, {'each_schedules_common_id': each_schedules_common_id, 'each_medicine_id': each_medicine_id})

      response_object = {
        'status': 'OK',
        'message': 'Successfully post schedules_common_id, medicines_id in schedules_medicines table.',
      }
      return response_object, 200
    except Exception as e:
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


def get_my_medicine_camera_info(data):
  """ Get my medicine camera information"""
  try:
    camera = data(['camera'])
    name = data(['name'])
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      if decoded_token:
        xmlUrl = 'http://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService'
        My_API_Ket = unquote('9BsX8qZyDtjw%2FX%2BvqnCiehTYarMxQrCvn75lSZyO%2Bxfz27GOcQ1aQMb1VvphiY%2FEHzXERrZO9z7cgprwNvtvdQ%3D%3D')
        queryParams = '?' + urlencode(
          {
            quote_plus('ServiceKey') : My_API_Key,
            quote_plus('item_name') : '',
            quote_plus('entp_no') : '',
            quote_plus('pageNo') : '',
            quote_plus('numOfRows') : '',
          }
        )
        response = {
          a: request.get(xmlUrl + queryParams).text.encode('utf-8')
        }

        response_object = {
          'status': 'OK',
          'message': 'Successfully get monthly checked.',
          'response': response
        }
        return response_object, 200
    except Exception as e:
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


def upload_medicine(data):
  """ Upload medicine information"""
  try:
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
      if decoded_token:

        image = Image.open(data)
        buffer = io.BytesIO()

        image = image.convert("RGB")
        # 해당 코드는 os 환경에서만 필요합니다. 배포시에는 안드로이드 버전 확인후 없애도 될듯합니다.

        image.save(buffer, "JPEG")
        buffer.seek(0)
        s3_connection = get_s3_connection()
        s3_connection.put_object(
              Body        = buffer,
              Bucket      = 'medisharp',
              Key         = f"{data.filename}_L",
              ContentType = data.content_type,
              ACL = 'public-read'
          )
        print('check3') 

        image_L_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{data.filename}_L"

        #print(image_L_url)
        return image_L_url, 200
    except Exception as e:
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





