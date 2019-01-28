from django.contrib import admin

# Register your models here.
from user.models import User, UserInfo, UserAddress

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(UserAddress)