import json

from django.shortcuts import render

# Create your views here.
import numpy as np
import base64
import pymongo as mongo
from datetime import date

from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from voiceEmotion.main import emotionCheck
from django import http
import wave
from faceEmotion.face import faceEmotion


@api_view(['GET', 'POST'])
def emotion(request):
    if request.method == "POST":

        # 음성 서버에 저장하는 작업
        audio_file = request.FILES.get('audio_data', None)

        obj = wave.open(audio_file, 'r')
        audio = wave.open('voiceEmotion/test.wav', 'wb')
        audio.setnchannels(obj.getnchannels())
        audio.setnframes(obj.getnframes())
        audio.setsampwidth(obj.getsampwidth())
        audio.setframerate(obj.getframerate())
        blob = audio_file.read()
        audio.writeframes(blob)

        # if audio_file is None:
        #     return http.HttpResponseBadRequest()
        #
        # # Mongo 클라이언트 생성
        # client1 = mongo.MongoClient()
        #
        # # 호스트와 포트를 지정
        # client2 = mongo.MongoClient('localhost', 27017)
        #
        # # 데이터베이스를 생성 혹은 지정
        # db = client1.face
        # db1 = client1.voice
        # dbs = client1.emotion_log
        #
        # id = request.session.get("user")
        #
        # DBFace = db[id]
        # DBVoice = db1[id]
        # DBEmotion = dbs[id]

        # 음성 체킹
        voiceresult = emotionCheck()

        # # Base 64 디코딩
        # print(request.POST['imgSrc'])
        # image = request.POST['imgSrc'].split(',')[1]
        # decoded_data = base64.b64decode(image)
        # np_data = np.fromstring(decoded_data, np.uint8)
        # faceYN, Fearful, Angry, Disgusting, Happy, Sad, Surprise, Neutral \
        #     = faceEmotion(request.session.get("user"), np_data)
        #
        # # 측정 값이 잘못된 경우 데이터 저장 예외처리
        # today = date.today()
        # if Fearful != 0:
        #     data = {"Face_Fearful": Fearful, "Face_Angry": Angry, "Face_Disgusting": Disgusting, "Face_Happy": Happy,
        #             "Face_Sad": Sad, "Face_Surprise": Surprise, "Face_Neutral": Neutral, "Date": str(today)}
        #     # 년 월 일 시 분 초 데이터 추가 (예정)
        #     DBFace.insert_one(data)
        # if voiceresult['fear'] != 0:
        #     data2 = {"Voice_Fear": float(voiceresult['fear']), "Voice_Neutral": float(voiceresult['neutral']),
        #              "Date": str(today)}
        #     # 년 월 일 시 분 초 데이터 추가 (예정)
        #     DBVoice.insert_one(data2)
        # if voiceresult['fear'] != 0 and Fearful != 0:
        #     data3 = {"Face_Fearful": Fearful, "Face_Angry": Angry, "Face_Disgusting": Disgusting, "Face_Happy": Happy,
        #              "Face_Sad": Sad, "Face_Surprise": Surprise, "Face_Neutral": Neutral,
        #              "Voice_Fear": float(voiceresult['fear']), "Voice_Neutral": float(voiceresult['neutral']),
        #              "Date": str(today)}
        #     DBEmotion.insert_one(data3)
        #
        # if voiceresult['neutral'] > 0.70:
        #     voiceYN = 'yes'
        # else:
        #     voiceYN = 'no'
        #
        # print(today)
        # data = {
        #     'faceYN': faceYN,
        #     'voiceYN': voiceYN,
        #     'face_positive': 1 - Fearful,
        #     'face_negative': Fearful,
        #     'voice_positive': voiceresult['neutral'],
        #     'voice_negative': voiceresult['fear']
        # }
        #
        # print(data)
        # # 만약 설정 조건이 맞을 경우 yes
        # if faceYN == 'yes' and voiceYN == 'yes':
        #     return Response({'data': data}, status=status.HTTP_200_OK)
        # # 아닐 경우 no
        # else:
        #     return Response({'data': data}, status=status.HTTP_200_OK)
        return Response({'data': 'data'}, status=status.HTTP_200_OK)

    # elif request.method == "POST":
    #     audio_file = request.FILES.get('audio_data', None)

    #
    #     obj = wave.open(audio_file, 'r')
    #     audio = wave.open('voiceEmotion/test.wav', 'wb')
    #     audio.setnchannels(obj.getnchannels())
    #     audio.setnframes(obj.getnframes())
    #     audio.setsampwidth(obj.getsampwidth())
    #     audio.setframerate(obj.getframerate())
    #     blob = audio_file.read()
    #     audio.writeframes(blob)
    #
    #     if audio_file is None:
    #         return http.HttpResponseBadRequest()
    #
    #     # voiceresult = emotionCheck()
    #
    #     return Response({'data': "success"}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def face(request):
    #
    # id = request.session.get("user")
    id = "admin"
    today = date.today()
    uuid_name = uuid4().hex;
    data_json = {
        "_id": uuid_name,
        "happy": request.POST['happy'],
        "angry": request.POST['angry'],
        "sad": request.POST['sad'],
        "fearful": request.POST['fearful'],
        "Date": str(today)
    }
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    db = client1.face
    DBFace = db[id]
    DBFace.insert_one(data_json)

    print(data_json)
    return Response({'data': data_json}, status=status.HTTP_200_OK)


@api_view(['UPDATE'])
def mypage_emotion(request):
    if request.method == "UPDATE":
        # voiceresult = emotionCheck()
        # faceresult = faceEmotion()

        # 사용자 아이디 조회를 통하여 보안 속성 가져오기

        # 만약 설정 조건이 맞을 경우 return 200

        # 아닐 경우 return 400

        return Response("ok", status=status.HTTP_200_OK)
