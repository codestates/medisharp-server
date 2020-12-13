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
import bs4
from datetime import time
from operator import itemgetter
from app.main import db
from app.main.model.medicines import Medicines
from app.main.model.users import Users
import requests, bs4
from lxml import html
import xml.etree
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import pandas as pd
from ..config import jwt_key, jwt_alg#, get_s3_connection, S3_BUCKET, S3_REGION, DevelopmentConfig #배포때는 여기를 ProductionConfig로 해주어야 합니다. 


def post_medicine(data):
  """Post medicine information"""
  try:  
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      if decoded_token:
        """직접등록하는 약에 대한 분기 코드는 비활성화 하겠습니다만, 저의 노고가(저 혼자) 아까워서 삭제는 안할게용 ㅠㅠ"""
        #현재 로그인된 유저아이디 값으로 등록된 모든 약의 아이디 값을 가져옴
        # engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI) #배포때는 여기를 ProductionConfig.SQLALCHEMY_DATABASE_URI 로 해주어야 합니다. 
        # query_find_medi_id = text("""SELECT medicines_id FROM users_medicines WHERE users_id = :each_users_id""")
        # with engine.connect() as con:
        #   result = con.execute(query_find_medi_id, {'each_users_id': user_id})
        # medicines_id = [row[0] for row in result]

        # #그리고 유저가 등록한 약들 중, 카메라로 촬영되지 않은 약만 가져온다.
        # res = []
        # res_name = []
        # for medicine_id in medicines_id:
        #     saved_medi = Medicines.query.filter(and_(Medicines.id==medicine_id, Medicines.camera==0)).first()
        #     if saved_medi:
        #       saved = {saved_medi.name : medicine_id}
        #       #saved[saved_medi.name] = medicine_id
        #       res_name.append(saved_medi.name)
        #       res.append(saved)
        # print('res:', res)

        medicine_ids = []
        for el in data:
          """카메라로 촬영된 경우에는, 유저 id 상관 없이(즉 다른 사람 user id로 등록된 약이더라도) 그냥 중복이 되면 안됩니다! 왜냐면 약에 대한 정보들은 공공API에서 불러오므로
          등록 유저 상관 없이 같은 약이면 모든 정보가 같을 것이니까요"""
          if el['camera']:
            saved_medi = Medicines.query.filter_by(name=el['name']).first()
            #카메라로 촬영된 약 정보가 이미 DB에 있다면 DB에 있는 id 값만 결과 list에 append
            if saved_medi:
              medicine_ids.append(saved_medi.id)
            else:
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

          else:       
            #아이디 값을 반복문을 돌면서, DB에서 해당하는 데이터를 가지고 나오고, DB에 저장된 약을 가상의 리스트에 저장
            # if el['name'] in res_name:
            #   for res_id in res:
            #     if el['name'] in res_id:
            #       medicine_ids.append(res_id[el['name']])
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


def post_users_medicines(data):
  """Post Users_id | medicines_id in schedules_medicines table"""
  try:
    medicines_id = data['medicines_id']

    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
      
      if decoded_token:
        engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI) #배포때는 여기를 ProductionConfig.SQLALCHEMY_DATABASE_URI 로 해주어야 합니다. 
        query = text("""INSERT INTO users_medicines(users_id, medicines_id) VALUES (:each_users_id, :each_medicine_id)""")
              
        with engine.connect() as con:
          for each_medicine_id in medicines_id:
            new_users_medicine = con.execute(query, {'each_users_id': user_id, 'each_medicine_id': each_medicine_id})

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
      
      if decoded_token:
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

def get_my_medicines():
  """ Get my medicines Information"""
  try:
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']

      if decoded_token:
        #reference: https://stackoverflow.com/questions/12593421/sqlalchemy-and-flask-how-to-query-many-to-many-relationship
        topic_fields = {
          'name': fields.String(required=True),
          'camera': fields.Boolean(required=True),
        }
        results = [marshal(topic, topic_fields) for topic in Medicines.query.filter(Medicines.taker.any(id=user_id)).all()]

        response_object = {
          'status': 'OK',
          'message': 'Successfully get my medicines.',
          'ressults': results
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


def strToBool(s):
  if s == 'true':
    return 1
  else:
    return 0


def get_my_medicines_info(data):
  """ Get my medicines Information by myself """
  try:
    camera = strToBool(data['camera'])
    name = data['name']
    try:
      token = request.headers.get('Authorization')
      decoded_token = jwt.decode(token, jwt_key, jwt_alg)
      user_id = decoded_token['id']
      if decoded_token:
        if camera == 1:
          url = 'http://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService/getMdcinPrductItem'
          MY_API_Key = unquote('9BsX8qZyDtjw%2FX%2BvqnCiehTYarMxQrCvn75lSZyO%2Bxfz27GOcQ1aQMb1VvphiY%2FEHzXERrZO9z7cgprwNvtvdQ%3D%3D')
          queryParams = '?' + urlencode(
            {
              quote_plus('ServiceKey') : MY_API_Key,
              quote_plus('item_name') : name, 
            }
            )
          response = requests.get(url + queryParams).text.encode('utf-8')
          xmlobj = bs4.BeautifulSoup(response, 'lxml-xml') 

          medicines = xmlobj.findAll('item')
          find_list = ["ITEM_NAME", "EE_DOC_DATA","UD_DOC_DATA", "VALID_TERM"]

          for i in find_list:
            for result in xmlobj.find_all(i):
              if i == "ITEM_NAME":
                print("약품명: ", result.text)
              elif i == "EE_DOC_DATA":
                for data in result.find_all("PARAGRAPH"):
                  print("효능효과: ", data.text)
              elif i == "UD_DOC_DATA":
                for data in result.find_all("PARAGRAPH"):
                  print("용법용량: ", data.text)
              elif i == "VALID_TERM":
                print("유효기간: ", result.text)
          
          response_object = {
            'status': 'OK',
            'message': 'Successfully get my medicines.',
            'results': xmlobj
          }
          return response_object, 200

        else:
          topic_fields = {
            'name': fields.String(required=True, description='medicine name'),
            'title': fields.String(description='personal description for this medicines'),
            'image_dir': fields.String(description='medicine image file path'),
            'effect': fields.String(description='medicine efficacy'),
            'capacity': fields.String(description='medicine dosage'),
            'validity': fields.String(description='medicine validity'),
            'camera': fields.Boolean(description='Whether to register as a camera')
          }
          results = [marshal(topic, topic_fields) for topic in Medicines.query.filter(and_(Medicines.taker.any(id=user_id), Medicines.camera==camera, Medicines.name==name)).all()]
  
          response_object = {
            'status': 'OK',
            'message': 'Successfully get my medicines.',
            'results': results
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