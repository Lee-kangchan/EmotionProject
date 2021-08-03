from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import pymongo as mongo
import datetime
# Create your views here.
from emotionSys.models import User, User_Security, Security


def main(request):

    user_email = request.session.get('user')
    if user_email is not None:
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs[user_email]
        data = {"log": "main", "date" : datetime.datetime.now()}
        DBLog.insert_one(data)

    request.method == 'GET'
    print(user_email)

    return render(request, 'index.html', {'field': user_email})


@csrf_exempt
def dashBoard(request):
    request.method == 'GET'
    user = request.session.get('user')
    user_email = request.session.get('user')
    gps = request.GET['gps']
    device = request.GET['device']

    if user_email is not None:
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs[user_email]
        data = {"log": "dashboard", "date": datetime.datetime.now(), "GPS": gps, "device": device}
        DBLog.insert_one(data)
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
    user_email = request.session.get('user')
    gps = request.GET['gps']
    device = request.GET['device']


    if user_email is not None:
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs[user_email]
        data = {"log": "emotion", "date": datetime.datetime.now(), "GPS": gps, "device": device}
        DBLog.insert_one(data)
    return render(request, 'check.html', {'field': user_email})


def emotion_result(request):
    request.method == 'GET'
    user_email = request.session.get('user')
    gps = request.GET['gps']
    device = request.GET['device']


    if user_email is not None:
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs[user_email]
        data = {"log": "emotion_result", "date": datetime.datetime.now(), "GPS": gps, "device": device}
        DBLog.insert_one(data)
    return render(request, 'result.html')

def emotion_face(request):
    request.method == 'GET'
    user_email = request.session.get('user')
    gps = request.GET['gps']
    device = request.GET['device']

    if user_email is not None:
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs[user_email]
        data = {"log": "emotion_face", "date": datetime.datetime.now(), "GPS": gps, "device": device}
        DBLog.insert_one(data)
    return render(request, 'face.html')
def re_auth(request):
    request.method == 'GET'
    user_email = request.session.get('user')

    gps = request.GET['gps']
    device = request.GET['device']
    if user_email is not None:
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs[user_email]
        data = {"log": "re_auth", "date": datetime.datetime.now(), "GPS": gps, "device": device}
        DBLog.insert_one(data)
    return render(request, 're_check.html')


def signOut(request):
    user_email = request.session.get('user')
    gps = request.GET['gps']
    device = request.GET['device']


    if user_email is not None:
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs[user_email]
        data = {"log": "signOut", "date": datetime.datetime.now(), "GPS": gps, "device": device}
        DBLog.insert_one(data)
    if request.session.get('user'):
        del (request.session['user'])
    return redirect('main')

def phone(request):
    if request.method == 'GET':
        user_email = request.session.get('user')
        gps = request.GET['gps']
        device = request.GET['device']


        if user_email is not None:
            # Mongo 클라이언트 생성
            client1 = mongo.MongoClient()
            dbs = client1.log
            DBLog = dbs[user_email]
            data = {"log": "phone", "date": datetime.datetime.now(), "GPS": gps, "device": device}
            DBLog.insert_one(data)
        return render(request, 'phonecheck.html')
@csrf_exempt
def signIn(request):
    if request.method == 'POST':
        user_email = request.session.get('user')

        if user_email is not None:
            # Mongo 클라이언트 생성
            client1 = mongo.MongoClient()
            dbs = client1.log
            DBLog = dbs[user_email]
            data = {"log": "signIn", "date": datetime.datetime.now()}
            DBLog.insert_one(data)
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']
        try:
            user = User.objects.get(user_email=user_email, user_pw=user_pw)

        except User.DoesNotExist:
            return render(request, 'index.html', {'error': 'not connect'})

        request.session['user'] = user.user_email
        return render(request, 'index.html', {'field': user_email})


def user_log2(request):
    if request.method == 'GET':
        user_email = request.session.get('user')
        gps = request.GET['gps']
        device = request.GET['device']

        if user_email is not None:
            # Mongo 클라이언트 생성
            client1 = mongo.MongoClient()
            dbs = client1.log
            DBLog = dbs[user_email]
            data = {"log": "user_log", "date": datetime.datetime.now(), "GPS": gps, "device": device}
            DBLog.insert_one(data);
        request.method == 'GET'
        user = request.session.get('user')

        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()

        # 호스트와 포트를 지정
        client2 = mongo.MongoClient('localhost', 27017)

        # 데이터베이스를 생성 혹은 지정
        dbs = client1.log

        id = request.session.get("user")

        DBEmotion = dbs[id]

        result = DBEmotion.find()

        return render(request, 'user_log2.html', {'data': result})

def user_log(request):
    if request.method == 'GET':
        user_email = request.session.get('user')
        gps = request.GET['gps']
        device = request.GET['device']

        if user_email is not None:
            # Mongo 클라이언트 생성
            client1 = mongo.MongoClient()
            dbs = client1.log
            DBLog = dbs[user_email]
            data = {"log": "user_log", "date": datetime.datetime.now(), "GPS": gps, "device": device}
            DBLog.insert_one(data);
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