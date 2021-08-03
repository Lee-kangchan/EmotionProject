from django.contrib import admin
from .models import User, AuthSms, Auth_Category

# Register your models here.

admin.site.register(User)
admin.site.register(AuthSms)
admin.site.register(Auth_Category)
