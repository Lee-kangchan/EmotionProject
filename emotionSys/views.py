from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import pymongo as mongo

# Create your views here.
from emotionSys.models import User, User_Security, Security


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
        user = User.objects.get(user_email=user)
        user_security = User_Security.objects.select_related("security").filter(user=user)
        print(user_security.values())
        print(user_security)
    except User.DoesNotExist:
        return render(request, 'index.html', {'error': 'not connect'})

    return render(request, 'dash.html', {"data": user_security, "user_data": user})


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

    return render(request, 're_check.html')


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
            user = User.objects.get(user_email=user_email, user_pw=user_pw)

        except User.DoesNotExist:
            return render(request, 'index.html', {'error': 'not connect'})

        request.session['user'] = user.user_email
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