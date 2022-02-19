from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.core import serializers
from .models import *
import uuid
import hashlib
import json


def f(request):
    return HttpResponse(request.session['cookie'])


class Index(View):
    def get(self, request):
        try:
            CustomUser.objects.get(cookie=request.session['cookie'])
            return redirect('main')
        except CustomUser.DoesNotExist:
            select = Class.objects.all()
            return render(request, 'digitalDR/about.html', {'select': select})


class MenuView(View):
    def get(self, request):
        user = check_user(request)
        if str(user) in ('Учитель', 'Ученик'):
            context = {
                'user': user
            }

            return render(request, 'digitalDR/menu.html', context=context)

        else:
            return user


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


class Login(View):
    def post(self, request):
        res = request.POST
        if res['mode'] == 'teacher':
            code = res['code']
            try:
                user = Teacher.objects.get(teacher_code=code)
                user.cookie = generate_s(40)
                user.save()
                request.session['cookie'] = user.cookie
                return JsonResponse({
                    'success': True,
                    'message': ''
                })
            except Teacher.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Данного кода не существует.'
                })


class Main(View):
    def get(self, request):
        user = check_user(request)
        if str(user) in ('Учитель', 'Ученик'):
            context = {
                'user': user
            }

            return render(request, 'digitalDR/main.html', context=context)

        else:
            return user


class RequestsStudents(View):
    def get(self, request):
        return render(request, '')


class Settings(View):
    def get(self, request):
        user = check_user(request)
        if str(user) in ('Учитель', 'Ученик'):
            context = {
                'user': user,
                'schoolId': user.card_num.split('-')[0],
                'cardId': user.card_num.split('-')[1],
                'dinner': dict(user.dinner_days),
                'lunch': dict(user.lunch_days)
            }

            return render(request, 'digitalDR/settings.html', context=context)

        else:
            return user

    def post(self, request):
        res = request.POST
        data = json.loads(res['data'])
        user = check_user(request)

        user.name = data['name'] if data['name'] else user.name
        user.last_name = data['lastName'] if data['lastName'] else user.last_name
        user.login = data['login'] if data['login'] else user.login
        user.email = data['email'] if data['email'] else user.email
        user.password = Password(data['password']).hash_password() if data['password'] else user.password
        user.card_num = data['card'] if data['card'] != '-' else user.card_num
        user.dinner_days = data['dinner']
        user.lunch_days = data['lunch']

        user.save()
        # user.update(
        #     name=data['name'],
        #     last_name=data['lastName'],
        #     email=data['email'],
        #     password=Password(data['password']).hash_password(),
        #     card_num=data['card'],
        #     dinner_days=data['dinner'],
        #     lunch_days=data['lunch']
        # )

        return JsonResponse({'succes': True})


def check_user(request):
    try:
        cookie = request.session['cookie']
        if Teacher.objects.filter(cookie=cookie):
            user = Teacher.objects.get(cookie=cookie)

        elif Student.objects.filter(cookie=cookie):
            user = Student.objects.get(cookie=cookie)

        else:
            return render(request, 'digitalDR/ERROR/KeyError.html')

        return user

    except KeyError:
        return render(request, 'digitalDR/ERROR/KeyError.html')


class Password:
    def __init__(self, password, username=None):
        self.salt = uuid.uuid4().hex
        self.password = password
        self.username = username

    def hash_password(self):
        return hashlib.sha256(self.salt.encode() + self.password.encode()).hexdigest() + ':' + self.salt

    def check_password(self, user_password):
        hashed_password = CustomUser.objects.filter(username=self.username)[0].password
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

