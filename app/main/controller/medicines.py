from flask import request, redirect, jsonify, make_response, render_template
from flask_restx import Resource
from werkzeug.utils import secure_filename
import requests
import numpy 
import cv2
import os
import matplotlib.pyplot as plt

from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import MedicineDto
import requests

api = MedicineDto.api

@api.route('/image')
class ImageUpload(Resource):
  def post(self):
    """카메라로 촬영한 이미지를 서버로 보내오고, 서버는 이 이미지를 출력하는 것 까지 확인해보는 API"""
    #나와 같이 400에러가 난다는 글 https://stackoverflow.com/questions/63633042/cant-upload-an-image-from-expo-react-native-and-post-to-a-flask-backend
    print("request: ", request.files)
    if 'image' not in request.files:
        print('No File Part')
    file = request.files['image']
    if file.filename == '':
        print('No Selected File')
    elif file and file.filename:
      filename = secure_filename(file.filename)
      print('filename is: ', filename)
      #read image file string data
      filestr = request.files['image'].read()
      # print("filestr: ", filestr)

      #convert string data to numpy array
      npimg = numpy.fromstring(filestr, numpy.uint8)
      print("npimg: ", npimg)
      # # convert numpy array to image
      img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
      print("img: ", img)

      filepath = os.path.join('/Users/jeonghyeonjeong/Desktop/medisharp/medisharp-server/clientimg', filename);
      file.save(img)