from flask import Flask 
from flask_cors import CORS

from users import users

app = Flask(__name__)
CORS(app)

app.register_blueprint(users, subdomain='users')


if not app.debug: 
    import logging
    from logging.handlers import RotatingFileHandler  
    file_handler = RotatingFileHandler(
          'medi_server.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.WARNING)  
    app.logger.addHandler(file_handler)


@app.before_first_request
def before_first_request():
    print("첫 실행입니다")
 
 
@app.before_request
def before_request():
    print("HTTP 요청이 들어왔습니다")
 
 
@app.after_request
def after_request(response):
    print("HTTP 요청 처리가 끝나고 브라우저에 응답하겠습니다")
    return response
    

@app.route("/") 
def hello(): 
    return "hello, world!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
