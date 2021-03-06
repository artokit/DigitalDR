from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='about'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('get_menu/', GetMenu.as_view(), name='get_menu'),
    path('login/', Login.as_view(), name='login'),
    path('settings/', Settings.as_view(), name='settings'),
    path('balance/', BalanceView.as_view(), name='balance'),
    path('requestsStudents/', RequestsStudents.as_view(), name='RequestsStudents'),
    path('orders/', Orders.as_view(), name='orders'),
    path('register/', Register.as_view(), name='register'),
    path('change/password/', ChangePassword.as_view(), name='ChangePassword'),
    path('change/foodMenu', ChangeFoodMenu.as_view(), name='ChangeFoodMenu'),
    path('logout/', user_logout, name='logout'),
    path('RequestsStudentsPost/', RequestsStudentsPost.as_view(), name='RequestsStudentsPost'),
    path('change/information/', ChangeUserInformationView.as_view(), name='ChangeUserInformation'),
]
