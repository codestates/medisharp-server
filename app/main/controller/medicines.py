import flask
from flask import request, redirect, jsonify, make_response, render_template
from flask_restx import Resource
from werkzeug.utils import secure_filename
import tensorflow
from keras.models import load_model
from keras.applications import ResNet50, imagenet_utils
from keras.preprocessing.image import img_to_array
from PIL import Image
import requests
import numpy as np
# import cv2
import os
import sys
import io
import jwt

from ..config import jwt_key, jwt_alg
from ..util.dto import MedicineDto
from ..service.medicines import post_medicine, post_schedules_common_medicines, upload_medicine
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from cnn.class_list import get_class_list

api = MedicineDto.api
# _medicines = MedicineDto.medicines

def prepare_image(image, target):
	if image.mode != "RGB":
		image = image.convert("RGB")

	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	return image

@api.route('/image')
class PredictMedicineName(Resource):
  def post(self):
    """카메라로 촬영한 이미지를 서버로 보내오고, 학습된 모델에서 예측결과를 client에게 전달해주는 API"""
    try: 
      class_list =  get_class_list()
      try:
        token = request.headers.get('Authorization')
        decoded_token = jwt.decode(token, jwt_key, jwt_alg)
        user_id = decoded_token['id']
        if decoded_token: 
          if 'image' not in request.files:
            response_object = {
            'status': 'Bad Request',
            'message': 'No File Part.',
            }
            return response_object, 400
          file = request.files['image']
          if file.filename == '':
            response_object = {
              'status': 'Bad Request',
              'message': 'No Selected File.',
              }
            return response_object, 400
          elif file and file.filename:
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image = prepare_image(image, target=(224, 224))
            currdir = os.getcwd()
            modeldir = os.path.join(currdir+ "/cnn/Pill_image_pretrained_mobile_model_2.h5")
            model = load_model(modeldir)
            preds = model.predict(image)
            pred_class = np.argmax(preds, axis=-1)
            prediction_result = class_list[int(pred_class)]
            print("prediction: ", class_list[int(pred_class)])
            response_object = {
              'status': 'OK',
              'message': 'Successfully predict image class.',
              'prediction': prediction_result
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


@api.route('')
class PostMedicine(Resource):
  def post(self):
    """Post Medicine API"""
    data = request.get_json().get('medicine') 
    return post_medicine(data)

@api.route('/upload')
class UploadMedicine(Resource):
  def post(self):
    """Upload Medicine API"""
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
      
@api.route('/schedules-medicines')
class PostSchedulesCommonMedicines(Resource):
  def post(self):
    """Post Schedules Common Medicines API"""
    data = request.get_json().get('schedules_common_medicines')
    return post_schedules_common_medicines(data)
