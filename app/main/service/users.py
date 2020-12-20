from app.main import db, create_app
from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
import json ,io, jwt, os
from sqlalchemy.sql import text
from sqlalchemy import and_ 
from app.main import db
from app.main.model.users import Users
from ..config import jwt_key, jwt_alg, MAIL_SENDER, MAIL_SENDER_PASSWORD
from string import punctuation, ascii_letters, digits
import random
from flask_mail import Message, Mail
import flask_bcrypt

app = create_app('dev') #배포시에는 prod

app.config.update(dict(
    DEBUG = True,
    MAIL_SUPPRESS_SEND = False,
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = MAIL_SENDER,
    MAIL_PASSWORD = MAIL_SENDER_PASSWORD,
))

mail = Mail(app)


def post_signup(data):
  """Post Login"""
  try:
    try:
      full_name = data['full_name']
      email = data['email']
      password = data['password']  
      mobile = data['mobile']
      login = 'basic'

      user = Users.query.filter_by(email=data['email']).first()

      if user == None:
        new_user = Users(
          full_name = data['full_name'],
          email = data['email'],
          password = data['password'], 
          mobile = data['mobile'],
          login = 'basic'
        )
        db.session.add(new_user)
        db.session.commit()

        response_object = {
          'status': 'OK',
          'message': 'Successfully Post Signup.',
        }
        return response_object, 200
    except Exception as e:
        db.session.rollback()
        print(e)
        response_object = {
          'status': 'fail',
          'message': 'Already a Registered User.',
        }
        return response_object, 409
    finally:
        db.session.close()
  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500


def send_password(send, receive, data):
    print(send, receive, data)
    try:
        msg = Message('약올림 임시 비밀번호입니다.', sender = send, recipients = [receive])
        msg.body = data
        msg.html = f'<p>{receive} 계정에 임시 변경된 비밀번호는 <strong>{data}<strong>입니다.<br>해당 비밀번호로 로그인 후 개인정보수정에 가셔서 비밀번호를 변경해주세요.</p>'
        mail.send(msg)
        return 'Sent'
    except Exception as e:
        print(e)
    finally:
        pass

def get_find_user(data):
  """Get Find User API"""
  try:
    try:
      email = data['email']

      user = Users.query.filter_by(email=email).first()
      print(user)
      if user:
        #임시비밀번호 발행   
        symbols = ascii_letters + digits + punctuation
        secure_random = random.SystemRandom()
        password = "".join(secure_random.choice(symbols) for i in range(10))
        print(password)
        send_password(MAIL_SENDER, email, password)

        result = {'id' : user.id, "password": password}

        response_object = {
          'status': 'OK',
          'message': 'Successfully post login.',
          'results': result
        }
        return response_object, 200
    except Exception as e:
      db.session.rollback()
      print(e)
      response_object = {
        'status': 'fail',
        'message': 'Unvaild Info. Try to Sign up or Social Login',
      }
      return response_object, 400
    finally:
      db.session.close()
  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500

def get_email_check(data):
  """get Email Check API"""
  try:
    try:
      email = data['email']
      search = db.session.query(Users).filter_by(email = email).first()
      print(search)

      if search is None:  
        response_object = {
          'status': 'OK',
          'message': '사용 가능한 이메일입니다.',
        }
        return response_object, 200
      else:
        response_object = {
        'status': 'fail',
        'message': '이미 가입되어있는 이메일입니다. 혹시 비밀번호를 잊으셨나요?',
        }
        return response_object, 400
    except Exception as e:
      print(e)
      response_object = {
        'status': 'fail',
        'message': '이미 가입되어있는 이메일입니다. 혹시 비밀번호를 잊으셨나요?',
      }
      return response_object, 400

  except Exception as e:
    response_object = {
      'status': 'Internal Server Error',
      'message': 'Some Internal Server Error occurred.',
    }
    return response_object, 500
      
def get_find_id(data):
  """Get Find ID API"""
  try:
    print(data)
    try:
      full_name = data['full_name']
      mobile = data['mobile']
      mobile_db = db.session.query(Users.mobile).filter(and_(Users.full_name==full_name, Users.login=='basic')).all()
      print(mobile_db)
      #print(flask_bcrypt.check_password_hash(mobile_db[0], mobile))

      result = None

      for el in mobile_db:
        if flask_bcrypt.check_password_hash(el[0], mobile):
          email = db.session.query(Users.email).filter(and_(Users.full_name==full_name, Users.mobile==el[0],Users.login=='basic')).first() 
          print(email)
          result = email

      if result:    
        response_object = {
          'status': 'OK',
          'message': 'Successfully Get Find ID.',
          'email': result
        }
        return response_object, 200
      else:
        response_object = {
        'status': 'fail',
        'message': 'Unvaild Info. Try to Sign up or Social Login',
        }
        return response_object, 404
    except Exception as e:
      db.session.rollback()
      print(e)
      response_object = {
        'status': 'fail',
        'message': 'Unvaild Info. Try to Sign up or Social Login.',
      }
      return response_object, 404
    finally:
      db.session.close()
  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500

def edit_temp_pw(data):
  """Get Find User API"""
  try:
    try:
      user_id = data['id']
      temp_pw = data['password']
      temp_pw_hash = flask_bcrypt.generate_password_hash(temp_pw)

      pw_changed = Users.query.filter_by(id =user_id).update({'password': temp_pw_hash})
      db.session.commit()

      response_object = {
        'status': 'OK',
        'message': 'Successfully changed to temporary password.',
      }
      return response_object, 200
    except Exception as e:
      print(e)
      db.session.rollback()
      response_object = {
        'status': 'fail',
        'message': 'fail to change password.',
      }
      return response_object, 400
    finally:
      db.session.close()
  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500  


def post_login(data):
  """Post Login"""
  try:
    try:
      email = data['email']
      password = data['password'] 
      user = Users.query.filter_by(email=email).first()
      if user:
        if flask_bcrypt.check_password_hash(user.password, password):
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
          'message': 'Unvalid user password.',
          }
          return response_object, 401
      else:
        response_object = {
          'status': 'fail',
          'message': 'Unvalid user email.',
        }
        return response_object, 401
    except Exception as e:
      db.session.rollback()
      print(e)
      response_object = {
        'status': 'fail',
        'message': 'Unvalid User.',
      }
      return response_object, 401
    finally:
      db.session.close()
  except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500

def social_signin(data):
    #print("profile_json:", data)
    # 받아온 데이터에서 쓸만한건 유저 닉네임이랑 id 정도더라구요.
    # 닉네임을 이메일처럼/ id를 비번처럼 활용하면 어떨까 했습니다.
    try:
      kakao_account = data.get("properties")
      email = kakao_account.get("nickname", None)
      kakao_id = str(data.get("id")) # 모델에서 비번을 str으로 설정했기 때문에 여기서 문자열로 변경안해주면 에러가!
      try:
        #print("kakao_account:", kakao_account)
        #print("email:", email)
        #print("kakao_id:", kakao_id)
        user = Users.query.filter_by(email=email).first() # 이메일값으로 쿼리 필터를 한번 해주고
        if not user: # 없으면 데이터를 생성합니다
          new_user = Users(
                email=email,
                password=kakao_id,
                full_name=email,
                mobile='null',
                login='social'
          )
          db.session.add(new_user)
          db.session.commit()
          print("user:", new_user.id)
          token = jwt.encode({"id":new_user.id}, jwt_key, jwt_alg) #그리고 저장했으니 토큰을 만들어줘야겠죠
          token = token.decode("utf-8")
          print("token:", token)
          response_object = {
              'status': 'success',
              'message': 'you become a member for our service',
              'Authorization': token
          }
          return response_object, 200 
        else: 
          user_id = user.id 
          print("user:", user_id)
          token = jwt.encode({"id":user_id}, jwt_key, jwt_alg) 
          token = token.decode("utf-8")
          #print("token:", token)
          response_object = {
              'status': 'already signin',
              'message': 'you already our member. login success',
              'Authorization': token
          }
          return response_object, 201
      except Exception as e:
        db.session.rollback()
        print(e)
        response_object = {
          'status': 'fail',
          'message': 'Provide a valid auth token.',
        }
        return response_object, 401
      finally:
        db.session.close()
    except Exception as e:
      response_object = {
        'status': 'Internal Server Error',
        'message': 'Some Internal Server Error occurred.',
      }
      return response_object, 500 


