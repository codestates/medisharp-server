from flask import request, redirect, jsonify, make_response
from flask_restx import Resource
from ..util.dto import MedicineDto
import requests
from ..service.medicines import post_medicine, post_schedules_common_medicines, upload_medicine, post_users_medicines, get_my_medicine_camera_info

api = MedicineDto.api
# _medicines = MedicineDto.medicines

@api.route('')
class PostMedicine(Resource):
  def post(self):
    """Post Medicine API"""
    data = request.get_json().get('medicine') 
    return post_medicine(data)

@api.route('/name/camera/true')
class GetMyMedicineCamaraInfo(Resource):
  def get(self):
    """Get My Medicine Camera Info API"""
    data = request.get_json().get('medicine') 
    return post_medicine(data)
    
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

"""
client에서
{
  "schedules_common_medicines":
  {
    "schedules_common_id": 1,
    "medicine_id": [1, 2, 3]
  }
}
이렇게 준다고 가정하고, 
schedules_medicines 테이블에
schedules_common_id | medicines_id
          1         |     1
          1         |     2
          1         |     3
이렇게 저장하는 것으로 구현
"""

@api.route('/users-medicines')
class PostUsersMedicines(Resource):
  def post(self):
    """Post Users Medicines API"""
    data = request.get_json().get('medicines_id')
    return post_users_medicines(data)

@api.route('/schedules-medicines')
class PostSchedulesCommonMedicines(Resource):
  def post(self):
    """Post Schedules Common Medicines API"""
    data = request.get_json().get('schedules_common_medicines')
    return post_schedules_common_medicines(data)

