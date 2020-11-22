from flask import request, redirect

from app.main import db
from app.main.model.users import Users


def social_signin():
    return Users.query.all()
  # if Account.objects.filter(kakao_id = kakao_id).exists():
        #     user = Account.objects.get(kakao_id = kakao_id)
        #     token = jwt.encode({"email" : email}, SECRET_KEY, algorithm = "HS256")
        #     token = token.decode("utf-8")

        #     return JsonResponse({"token" : token}, status=200)

        # else :
        #     Account(
        #         kakao_id = kakao_id,
        #         email    = email,
        #     ).save()

        #     token = jwt.encode({"email" : email}, SECRET_KEY, algorithm = "HS256")
        #     token = token.decode("utf-8")

        #     return JsonResponse({"token" : token}, status = 200)