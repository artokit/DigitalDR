from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, FormView, TemplateView
from .utils import DataMixin
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.core import serializers
from .models import *
import uuid
import hashlib
import json
import requests
from .forms import UserChange
import datetime


def check_balance(card):
    url = 'http://xn--58-6kc3bfr2e.xn--p1ai/ajax/'

    data = {
        'card': card,
        'act': 'FreeCheckBalance'
    }

    r = requests.post(url, data)

    return r.json()['text']


class Main(TemplateView):
    pass


class Index(TemplateView):
    template_name = 'digitalDR/about.html'


class MenuView(DataMixin, ListView):
    template_name = 'digitalDR/menu.html'
    model = Menu

    def get_queryset(self):
        return Menu.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return {**context, **self.get_user_context(user=self.request.user)}


class GetMenu(View):
    def get(self, request):
        menu = Menu.objects.all()
        return HttpResponse(serializers.serialize('json', menu), content_type='application/json')


class AddUser(View):
    def post(self, request):
        res = dict(request.POST)
        d = {
            'first_name': ['Имя', 'id_first_name'],
            'last_name': ['Фамилия', 'id_last_name'],
            'email': ['Email', 'id_email'],
            'username': ['Логин', 'id_username'],
            'password': ['Пароль', 'id_password1'],
            'user_class': ['Класс', 'id_select_class']
        }

        for i in res:
            if not res[i][0]:
                return JsonResponse({
                    'success': False,
                    'message': f'Вы не заполнили поле {d[i][0]}.',
                    'elem_error_id': d[i][1]
                })

        if Student.objects.filter(username=res['username'][0]):
            return JsonResponse({
                'success': False,
                'message': 'Аккаунт с данным логином уже создан.',
                'elem_error_id': d['username'][1]
            })

        if len(res['email'][0].split('@')) != 2:
            return JsonResponse({
                'success': False,
                'message': 'Введите корректный Email.',
                'elem_error_id': d['email'][1]
            })

        if Student.objects.filter(email=res['email'][0]):
            return JsonResponse({
                'success': False,
                'message': 'Аккаунт с данным Email уже существует.',
                'elem_error_id': d['email'][1]
            })

        if not Class.objects.filter(name_class=res['user_class'][0]):
            return JsonResponse({
                'success': False,
                'message': 'Такого класса не существует.',
                'elem_error_id': d['user_class'][1]
            })

        user = Student(**{
            'name': res['first_name'][0],
            'last_name': res['last_name'][0],
            'email': res['email'][0],
            'username': res['username'][0],
            'password': Password(res['password'][0]).hash_password(),
            'user_class': Class.objects.get(name_class=res['user_class'][0])
        })

        user.cookie = (lambda: generate_s(40))()

        user.save()

        request.session['cookie'] = user.cookie
        return JsonResponse({'success': True})


class RequestsStudents(DataMixin, ListView):
    template_name = 'digitalDR/requestsStudents.html'
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return {**context, **self.get_user_context(user=self.request.user)}


class Settings(DataMixin, FormView):
    form_class = UserChange
    template_name = 'digitalDR/settings.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return {**context, **self.get_user_context(user=self.request.user)}

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)


class Balance(View):
    pass


class Login(LoginView):
    template_name = 'digitalDR/login.html'
    form_class = AuthenticationForm


class Orders(DataMixin, ListView):
    template_name = 'digitalDR/orders.html'
    model = User
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        teacher_class = Class.objects.get(user=self.request.user)
        context['lunch_count'] = 0
        context['dinner_count'] = 0

        for user in teacher_class.user.all():
            menu = UserMenu.objects.get(user=user)
            today = datetime.datetime.today().weekday()

            if list(menu.dinner_days.values())[today]:
                context['dinner_count'] += 1

            if list(menu.lunch_days.values())[today]:
                context['lunch_count'] += 1

        return {**context, **self.get_user_context(user=self.request.user)}

    def get_queryset(self):
        teacher_class = Class.objects.get(user=self.request.user)
        return {user: UserMenu.objects.get(user=user) for user in teacher_class.user.all()}


class Password:
    def __init__(self, password):
        self.salt = uuid.uuid4().hex
        self.password = password

    def hash_password(self):
        return hashlib.sha256(self.salt.encode() + self.password.encode()).hexdigest() + ':' + self.salt

    def check_password(self, user_password):
        hashed_password = self.password
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

