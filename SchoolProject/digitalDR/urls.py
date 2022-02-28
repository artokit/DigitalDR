from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='about'),
    path('menu', MenuView.as_view(), name='menu'),
    path('get_menu', GetMenu.as_view(), name='get_menu'),
    path('add_user', AddUser.as_view(), name='add_user'),
    path('login', Login.as_view(), name='login'),
    path('main', Main.as_view(), name='main'),
    path('settings', Settings.as_view(), name='settings'),
    path('balance', Balance.as_view(), name='balance'),
    path('requestsStudents', RequestsStudents.as_view(), name='RequestsStudents'),
    path('orders/', Orders.as_view(), name='orders')
]
