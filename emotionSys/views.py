import base64
import hashlib
import hmac
import time
import json
from random import randint

import requests
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import pymongo as mongo

# Create your views here.
from requests import Response
from rest_framework import status
from rest_framework.utils import json

from emotionSys.models import User, AuthSms, Auth_Category  # , User_Security, Security
from my_settings import EMAIL


def main(request):
    request.method == 'GET'
    user_email = request.session.get('user')
    print(user_email)

    return render(request, 'index.html', {'field': user_email})


@csrf_exempt
def dashBoard(request):
    request.method == 'GET'
    user = request.session.get('user')
    try:
        user = User.objects.get(email=user)

        if user.type == 'admin':
            auth_category = Auth_Category.objects.all()

            print(auth_category)
            return render(request, 'dash.html', {"user_data": user, "auth_category": auth_category})

        # else :

        # user_security = User_Security.objects.select_related("security").filter(user=user)

        # return render(request, 'dash.html', {"user_data": user, "user_auth": user_auth})

        # user_security = User_Security.objects.select_related("security").filter(user=user)
        # print(user_security.values())
        # print(user_security)
    except User.DoesNotExist:
        return render(request, 'index.html', {'error': 'not connect'})

    # return render(request, 'dash.html', {"data": user_security, "user_data": user})
    return render(request, 'dash.html', {"user_data": user})


def emotion(request):
    request.method == 'GET'
    user_email = request.session.get('user_email')

    return render(request, 'check.html', {'field': user_email})


def emotion_result(request):
    request.method == 'GET'

    return render(request, 'result.html')


def emotion_face(request):
    request.method == 'GET'

    return render(request, 'face.html')


def re_auth(request):
    request.method == 'GET'

    # user = request.session.get('user')
    try:
        # user = User.objects.get(email=user)

        auth_category = Auth_Category.objects.all()

        print(auth_category)
        return render(request, 're_check.html', {"auth_category": auth_category})

    except User.DoesNotExist:
        return render(request, 're_check.html', {'error': 'not connect'})


def signOut(request):
    if request.session.get('user'):
        del (request.session['user'])
    return redirect('main')


def phone(request):
    if request.method == 'GET':
        return render(request, 'phonecheck.html')


@csrf_exempt
def signIn(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']
        try:
            user = User.objects.get(email=user_email, password=user_pw)

        except User.DoesNotExist:
            return render(request, 'index.html', {'error': 'not connect'})

        request.session['user'] = user.email
        return render(request, 'index.html', {'field': user_email})


def user_log(request):
    if request.method == 'GET':
        request.method == 'GET'
        user = request.session.get('user')

        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()

        # 호스트와 포트를 지정
        client2 = mongo.MongoClient('localhost', 27017)

        # 데이터베이스를 생성 혹은 지정
        # db = client1.face
        # db1 = client1.voice
        dbs = client1.emotion_log

        id = request.session.get("user")

        # DBFace = db[id]
        # DBVoice = db1[id]
        DBEmotion = dbs[id]

        result = DBEmotion.find()

        return render(request, 'user_log.html', {'data': result})


def email_sign(request):
    if request.method == 'GET':
        current_site = get_current_site(request)
        print(current_site)

        domain = current_site.domain
        mail_title = "이메일 2차 인증을 완료해주세요"
        message_data = "https://192.168.64.94:8000/users/check"
        email = EmailMessage(mail_title, message_data, to=['20161658@g.dongseo.ac.kr'])

        email.send()

        return JsonResponse({"message": "SUCCESS"}, status=200)


def activate(request):
    if request.method == 'GET':
        return redirect(EMAIL['REDIRECT_PAGE'])


def check_sms(request):
    if request.method == 'POST':
        user_email = request.session.get('user')
        input_data = request.POST['number']

        user = User.objects.get(email=user_email)
        auth = AuthSms.objects.get(auth_phone=user.phone)

        if int(input_data) == int(auth.auth_number):
            return render(request, 'approval.html')

        else:
            return render(request, 're_check.html')


timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

url = "https://sens.apigw.ntruss.com"
requestUrl1 = "/sms/v2/services/"
requestUrl2 = "/messages"
serviceId = "ncp:sms:kr:266490177325:dsu_emotion"
access_key = "QRqgBlLhOPVszA8iAyXJ"

uri = requestUrl1 + serviceId + requestUrl2
apiUrl = url + uri


def make_signature():
    secret_key = "X8bxpHlTti6oFR3dg7cND3WwqquCV5lIb7OGy1qT"
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')

    key = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    return key


class AuthSmsView(View):

    # def send_sms(self, auth_phone, auth_number):
    #
    #     messages = {"to": str(auth_phone)}
    #
    #     data = {
    #         'type': 'SMS',
    #         'contentType': 'COMM',
    #         'countryCode': '82',
    #         'from': "01093964847",
    #         'content': "인증번호 : " + str(auth_number),
    #         'messages': [messages]
    #     }
    #     body2 = json.dumps(data)
    #
    #     headers = {
    #         'Content-Type': 'application/json; charset=utf-8',
    #         'x-ncp-apigw-timestamp': timestamp,
    #         'x-ncp-iam-access-key': access_key,
    #         'x-ncp-apigw-signature-v2': make_signature(),
    #     }
    #
    #     res = requests.post(apiUrl, headers=headers, data=body2)

    def get(self, request):
        try:
            user_email = request.session.get('user')
            user = User.objects.get(email=user_email)

            # input_data = json.loads(request.body)
            # input_phone_number = input_data['auth_phone']
            input_phone_number = user.phone
            created_auth_number = randint(1000, 10000)
            exist_phone_number = AuthSms.objects.get(auth_phone=input_phone_number)
            exist_phone_number.auth_number = created_auth_number
            exist_phone_number.save()
            self.send_sms(auth_phone=input_phone_number, auth_number=created_auth_number)

            return render(request, 'authSms.html')

        except AuthSms.DoesNotExist:
            AuthSms.objects.create(
                auth_phone=input_phone_number,
                auth_number=created_auth_number
            ).save()

            self.send_sms(auth_phone=input_phone_number, auth_number=created_auth_number)

            return render(request, 'authSms.html')


def v2_main(request):
    if request.method == 'GET':

        user_email = request.session.get('user_email')

        if user_email is None:
            return render(request, 'index.html')

        else:
            user = User.objects.get(email=user_email)
            request.session['user_email'] = user.email

            print(user.name)
            return render(request, 'index.html', {'data': user.name})


def v2_signIn(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']
        try:
            user = User.objects.get(email=user_email, password=user_pw)

        except User.DoesNotExist:
            return render(request, 'index.html', {'error': 'No signIN'})

        request.session['user_email'] = user.email
        return render(request, 'index.html', {'data': user.name})


def v2_signUp(request):
    if request.method == 'GET':
        return render(request, 'register.html')


    elif request.method == 'POST':
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']

        User.objects.create(
            email=user_email,
            password=user_pw
        ).save()

        return render(request, 'index.html')


def v2_fail(request):
    if request.method == 'GET':
        auth_category = Auth_Category.objects.all()

        return render(request, 'check.html', {'data': auth_category})


def v2_emailCheck(request):
    if request.method == 'GET':
        user_email = request.session.get('user_email')

        return render(request, 'emailCheck.html', {'data': user_email})


class v2_phoneCheck(View):

    def send_sms(self, auth_phone, auth_number):

        messages = {"to": str(auth_phone)}

        data = {
            'type': 'SMS',
            'contentType': 'COMM',
            'countryCode': '82',
            'from': "01093964847",
            'content': "인증번호 : " + str(auth_number),
            'messages': [messages]
        }
        body2 = json.dumps(data)

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': access_key,
            'x-ncp-apigw-signature-v2': make_signature(),
        }

        res = requests.post(apiUrl, headers=headers, data=body2)

    def get(self, request):

        try:
            user_email = request.session.get('user_email')
            user = User.objects.get(email=user_email)

            # input_data = json.loads(request.body)
            # input_phone_number = input_data['auth_phone']
            input_phone_number = user.phone
            created_auth_number = randint(1000, 10000)
            exist_phone_number = AuthSms.objects.get(auth_phone=input_phone_number)
            exist_phone_number.auth_number = created_auth_number
            exist_phone_number.save()
            self.send_sms(auth_phone=input_phone_number, auth_number=created_auth_number)

            return render(request, 'phoneCheck.html', {'data': user.phone})

        except AuthSms.DoesNotExist:
            AuthSms.objects.create(
                auth_phone=input_phone_number,
                auth_number=created_auth_number
            ).save()

            self.send_sms(auth_phone=input_phone_number, auth_number=created_auth_number)

            return render(request, 'phoneCheck.html', {'data': user.phone})

    def post(self, request):

        user_email = request.session.get('user_email')
        input_data = request.POST['number']

        user = User.objects.get(email=user_email)
        auth = AuthSms.objects.get(auth_phone=user.phone)

        if int(input_data) == int(auth.auth_number):
            return render(request, 'index.html')

        else:
            return render(request, 'check.html')


# def v2_locateCheck(request):
#     if request.method == 'GET':
#
#         if(false)
#             return render(request, 'check.html')
#
#         else
#             return render(request, 'index.html')


def v2_dashBoard(request):
    if request.method == 'GET':

        user_email = request.session.get('user_email')

        user = User.objects.get(email=user_email)

        if user.type == 'admin':
            auth_category = Auth_Category.objects.all()

            client1 = mongo.MongoClient()
            client2 = mongo.MongoClient('localhost', 27017)

            dbs = client1.emotion_log

            id = request.session.get("user_email")

            DBEmotion = dbs[id]

            result = DBEmotion.find()
            return render(request, 'profile.html', {"auth_category": auth_category,
                                                    "data": result})

        else:

            return render(request, 'profile.html')
