from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from .models import CustomUser


admin.site.register(CustomUser)
admin.site.register(Menu)
admin.site.register(Class)
admin.site.register(Cookie)