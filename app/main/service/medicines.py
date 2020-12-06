from flask import request, jsonify, redirect
from flask_restx import Resource, fields, marshal
from sqlalchemy import and_
import json, jwt, re, numpy, cv2, os, io, uuid, base64
from app.main import db
from PIL import Image
from app.main.model.medicines import Medicines
from ..config import jwt_key, jwt_alg , get_s3_connection, S3_BUCKET, S3_REGION


def upload_img_s3(img_str):
  print('img_str.filename:',img_str.filename) 
  # 해당 파일 이름으로 S3에 저장되는데, 지금은 클라이언트에서 임의로 지정한
  # form_data.append('image', blob); 해당 코드의 blob 이름으로 오고 있습니다. 
  # 그런데 해당 이름은 유저가 설정한 이름으로 저장해야 하다보니, S3에 이미지가 저장되는 시점을 결정해야 할듯해요.

  unique_id = str(uuid.uuid4().int)
  s3_connection = get_s3_connection()

  s3_connection.put_object(
        Body        = img_str,
        Bucket      = S3_BUCKET,
        Key         = f"{unique_id}_{img_str.filename}_L",
        ContentType = img_str.content_type,
        ACL = 'public-read'
    )

  image_L_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{unique_id}_{img_str.filename}_L"
 

  return image_L_url
