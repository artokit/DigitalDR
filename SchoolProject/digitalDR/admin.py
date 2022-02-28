from django.contrib import admin
from .models import *
from .models import CustomUser


admin.site.register(CustomUser)
admin.site.register(Menu)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(UserMenu)
