from flask import request, redirect, jsonify, make_response
from flask_restx import Resource
from ..util.dto import MedicineDto
import requests
from ..service.medicines import post_medicine

api = MedicineDto.api
# _medicines = MedicineDto.medicines

"""
클라에서 Request로 주는 약 정보
{
  "medicine": [
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
    }
  ]
}
라고 생각하고 구현
"""
@api.route('/upload')
class UploadMedicine(Resource):
  def post(self):
    """Post Medicine API"""
    print("request: ", request.files)
    if 'image' not in request.files:
      print('No File Part')
    file = request.files['image']
    if file.filename == '':
      print('No Selected File')
    elif file and file.filename:
      filename = secure_filename(file.filename)
      filestr = request.files['image'].read()
      print('file:',file)
      print('filename:',filename)
      print('type:',file.content_type)
      #print('filestr:',filestr)
      return upload_medicine(file)