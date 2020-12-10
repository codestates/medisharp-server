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
import cv2
import os
import sys
import io

from ..util.dto import MedicineDto
from ..service.medicines import post_medicine, post_schedules_common_medicines, upload_medicine

api = MedicineDto.api
# _medicines = MedicineDto.medicines

# 2단계 상윞폴더 경로를 추가하는 방법: https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from cnn.class_list import get_class_list

# def load_model():
# 	global model
# 	model = load_model('/Users/jeonghyeonjeong/Desktop/medisharp-server/cnn/Pill_image_pretrained_mobile_model_2.h5')


def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")

	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return image

@api.route('/image')
class ImageUpload(Resource):
  def post(self):
    """카메라로 촬영한 이미지를 서버로 보내오고, 학습된 모델에서 예측결과를 client에게 전달해준는 API"""
    print("알약 list: ", get_class_list()) #잘 찍힌다. 
    # print("request: ", request.files)
    # if 'image' not in request.files:
    #     print('No File Part')
    # file = request.files['image']
    # if file.filename == '':
    #     print('No Selected File')
    # elif file and file.filename:
    #   image = flask.request.files["image"].read()
    #   image = Image.open(io.BytesIO(image))

    #   # preprocess the image and prepare it for classification 
    #   image = prepare_image(image, target=(224, 224))

    #   # model
    #   model = load_model('/Users/jeonghyeonjeong/Desktop/medisharp-server/cnn/Pill_image_pretrained_mobile_model_2.h5') 
      
    #   # classify the input image and then initialize the list
		# 	# of predictions to return to the client
    #   # preds = model.predict(image)
    #   preds = model.predict(image)
			
    #   pred_class = np.argmax(preds, axis=-1)
    #   prediction_result = class_list[int(pred_class)]
    #   print("prediction: ", class_list[int(pred_class)])#prediction:  이연클래리트로마이신정500밀리그램   

    #   response_object = {
    #     'status': 'OK',
    #     'message': 'Successfully predict image class.',
    #     'prediction': prediction_result
    #   }
    #   return response_object, 200

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

