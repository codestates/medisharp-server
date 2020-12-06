from flask import request, redirect, jsonify, make_response, render_template
from flask_restx import Resource
from werkzeug.utils import secure_filename
import requests
import numpy 
import cv2
import os

# import the necessary packages
import tensorflow
from keras.models import load_model
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io

from flask import request, redirect, jsonify, make_response
from flask_restx import Resource

from ..util.dto import MedicineDto
import requests

api = MedicineDto.api

# def load_model():
# 	global model
# 	model = load_model('/Users/jeonghyeonjeong/Desktop/medisharp-server/cnn/Pill_image_pretrained_mobile_model_2.h5')


class_list = ['가네탑에스연질캡슐',
 '가바로닌캡슐100mg',
 '가바틴캡슐300밀리그람',
 '나리센연질캡슐',
 '나이시드캡슐150㎎',
 '나프민캡슐',
 '네오로신캡슐',
 '넥사졸캡슐20밀리그램',
 '넬슨세픽심캡슐',
 '누코미트캡슐200밀리그램',
 '뉴로낙CR정',
 '뉴트로필정',
 '다이뉴에이치알정',
 '다이피릴엠정2',
 '대우세파클러캡슐250밀리그램',
 '독시라마이신캡슐100mg',
 '동인당은행엽엑스정',
 '두타반플러스정',
 '드로본정150밀리그램',
 '디',
 '디젠정',
 '레벡스캡슐',
 '로텐연질캡슐',
 '로페란캡슐',
 '리드덴타캡슐',
 '리드미캡슐',
 '리리베아캡슐75mg',
 '리버플란연질캡슐',
 '린코신캡슐',
 '메바론정',
 '뮤코원캡슐',
 '베아라제정',
 '벤포킹정',
 '보령독시플루리딘캡슐100밀리그램',
 '복합쓸기담연질캡슐',
 '부코펜정',
 '브라덱신캡슐',
 '비스펜틴조절방출캡슐10mg',
 '비타마인연질캡슐',
 '비타코플러스연질캡슐',
 '빅톤연질캡슐',
 '빅파워비타연질캡슐',
 '삼진제테파캅셀',
 '설포린캡슐',
 '세푸르엠정250mg',
 '세프로캅셀',
 '셀막비타연질캡슐',
 '셀벡스캡슐',
 '스파졸캡슐',
 '시세틴20밀리그램캡슐',
 '실로스타엠서방캡슐200밀리그램',
 '실로스탄씨알정200밀리그램',
 '씨베리움캡슐',
 '아노벤캅셀',
 '아세테밍정',
 '아세트라셋정',
 '아웃콜코정',
 '아웃콜코프캡슐',
 '아크랑캅셀',
 '아트렌캡슐50밀리그램',
 '알리코이부프로펜정400mg',
 '알마믹스정',
 '알보젠레날리도마이드캡슐5밀리그램',
 '에니트정10',
 '에도날캡슐',
 '에란탄지속정60밀리그램',
 '에카린에이정',
 '엘도브론캡슐300밀리그램',
 '엠지비타-에프정',
 '엠지비타에프정',
 '오스가바캡슐100밀리그램',
 '옥트산에이치알정',
 '원트란서방정',
 '유로비트에스알캡슐4밀리그람',
 '이연클래리트로마이신정500밀리그램',
 '잘보빈정500밀리그램',
 '제로픽스정1밀리그램',
 '제트-유정',
 '조인사민캡슐',
 '콘서타OROS서방정54밀리그램',
 '콘티푸로스연질캡슐',
 '쿨노즈캡슐',
 '큐리티연질캡슐',
 '타이노즈연질캡슐',
 '타이레놀정500밀리그람',
 '타크로리캡슐0',
 '타크로스캡슐0',
 '탑픽스정1밀리그램',
 '트라마롤세미정',
 '트라마펜정',
 '파미버정',
 '팜슈어정750밀리그램',
 '프로부펜정400밀리그램',
 '프로세틴캡슐20mg',
 '프리린캡슐150밀리그램',
 '프릭딘캡슐10mg',
 '피도글에이캡슐',
 '피엠에스리스페리돈정0',
 '하디디앤엔연질캡슐',
 '하모빅캡슐',
 '헤파라이프연질캡슐350mg',
 '휴온스니자티딘캡슐150mg']

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
    #나와 같이 400에러가 난다는 글 https://stackoverflow.com/questions/63633042/cant-upload-an-image-from-expo-react-native-and-post-to-a-flask-backend
    print("request: ", request.files)
    if 'image' not in request.files:
        print('No File Part')
    file = request.files['image']
    if file.filename == '':
        print('No Selected File')
    elif file and file.filename:
      image = flask.request.files["image"].read()
      image = Image.open(io.BytesIO(image))

      # preprocess the image and prepare it for classification 
      image = prepare_image(image, target=(224, 224))

      # model
      model = load_model('/Users/jeonghyeonjeong/Desktop/medisharp-server/cnn/Pill_image_pretrained_mobile_model_2.h5') 
      
      # classify the input image and then initialize the list
			# of predictions to return to the client
      # preds = model.predict(image)
      preds = model.predict(image)
			
      pred_class = np.argmax(preds, axis=-1)
      prediction_result = class_list[int(pred_class)]
      print("prediction: ", class_list[int(pred_class)])#prediction:  이연클래리트로마이신정500밀리그램   

      response_object = {
        'status': 'OK',
        'message': 'Successfully predict image class.',
        'prediction': prediction_result
      }
      return response_object, 200





      









      # print('before filename is: ', file.filename)
      # filename = secure_filename(file.filename)
      # print('filename is: ', filename)
      # #read image file string data
      # filestr = request.files['image'].read()
      # # print("filestr: ", filestr)

      # #convert string data to numpy array
      # npimg = numpy.fromstring(filestr, numpy.uint8)
      # print("npimg: ", npimg)
      # #convert numpy array to image
      # img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
      # print("img: ", img.shape) #img:  (720, 1280, 3)으로 나옴 
      # #reshape 필요
      # img = Image.fromarray(img)
      # img = img.resize((224, 224))
      # print("after img: ", img) #after img:  <PIL.Image.Image image mode=RGB size=224x224 at 0x7FCB6FE40128> (224, 224)로 사이즈 조정됨. 

      # print("이미지 형식 출력", img.format)#이미지 형식 출력 None

      # print("이미지 크기 출력", img.size)#이미지 크기 출력 (224, 224)

      # print("이미지 mode 출력", img.mode)#이미지 mode 출력 RGB
      # # # preprocess the image and prepare it for classification
      # # image = imagenet_utils.preprocess_input(img)
      # # print("image: ", image)

      # # model
      # model = load_model('/Users/jeonghyeonjeong/Desktop/medisharp-server/cnn/Pill_image_pretrained_mobile_model_2.h5') 
      
      # # classify the input image and then initialize the list
			# # of predictions to return to the client
      # # preds = model.predict(image)
      # preds = model.predict(img)
			
      # print("prediction: ", preds)