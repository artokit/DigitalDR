from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='about'),
    path('menu', MenuView.as_view(), name='menu'),
    path('get_menu', GetMenu.as_view(), name='get_menu'),
    path('add_user', AddUser.as_view(), name='add_user'),
    path('f', f, name='f'),
    path('login', Login.as_view(), name='login'),
]
