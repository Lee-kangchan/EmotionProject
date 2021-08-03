from django.urls import path
from . import views

urlpatterns = [
    path('main', views.main, name='main'),
    path('emotion', views.emotion, name='emotion'),
    path('face2', views.emotion_face, name='emotion_face'),
    path('emotion/result', views.emotion_result, name='emotion_result'),
    path('signIn', views.signIn, name='signIn'),
    path('signOut', views.signOut, name='signOut'),
    path('phone', views.phone, name='phone'),
    # path('singUp/', views.singUp, name='singUp'),
    path('dashBoard', views.dashBoard, name='dashBoard'),
    path('re_auth', views.re_auth, name='re_auth'),
    path('userlog', views.user_log, name='user_log'),
    path('userlog2', views.user_log2, name='user_log2'),
]
