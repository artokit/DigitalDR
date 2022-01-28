from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='about'),
    path('menu', menu, name='menu'),
    path('get_menu', get_menu, name='get_menu'),
]
