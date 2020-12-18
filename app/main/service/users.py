#-*- coding: utf-8 -*-
# users 테이블에 관련된 쿼리문 작성하는 파일
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_ , create_engine
import json ,io
from sqlalchemy.sql import text
import jwt
import bcrypt
import flask_mail
from app.main import db
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg , get_s3_connection, S3_BUCKET, S3_REGION, DevelopmentConfig #배포때는 여기를 ProductionConfig로 해주어야 합니다. 
from string import punctuation, ascii_letters, digits

def get_find_user(data):
  """Get Find User API"""
  try:
    try:
      email = data['email']
      
      user = Users.query.filter_by(email=email).first()
      print(user)
      if user:
        id = db.session.query(User.id).filter(User.email==email).all() 

        #임시비밀번호 발행   
        symbols = ascii_letters + digits + punctuation
        secure_random = random.SystemRandom()
        password = "".join(secure_random.choice(symbols) for i in range(10))   

        #이메일 보내기
        def mail():
          msg = Message('약올림 임시 비밀번호입니다.', recipients=email)
          mail.send(msg)
          return 'Sent'
 
        response_object = {
          'status': 'OK',
          'message': 'Successfully post login.',
          'id': users_id
        }
        return response_object, 200
    except Exception as e:
      print(e)
      response_object = {
        'status': 'fail',
        'message': '일치하는 회원 정보가 없습니다.',
      }
      return response_object, 400

  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500 