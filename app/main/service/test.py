#user 모델에 관련된 쿼리문 작성 파일
from app.main import db
from app.main.model.users import Users

def get_all_users():
    return Users.query.all()
