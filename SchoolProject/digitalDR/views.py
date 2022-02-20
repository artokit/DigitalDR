from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.core import serializers
from .models import *
import uuid
import hashlib
import json
import requests


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


def check_balance(card):
    url = 'http://xn--58-6kc3bfr2e.xn--p1ai/ajax/'

    data = {
        'card': card,
        'act': 'FreeCheckBalance'
    }

    r = requests.post(url, data)

    return r.json()['text']


class Index(View):
    def get(self, request):
        user = check_user(request)
        if str(user) in ('Учитель', 'Ученик'):
            context = {
                'user': user
            }

            return redirect('main')

        else:
            return render(request, 'digitalDR/about.html', context={'select': Class.objects.all()})


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

        else:
            login = res['login']
            password = res['password']
            try:
                user = CustomUser.objects.get(username=login)
                if Password(user.password).check_password(password):
                    user.cookie = generate_s(40)
                    user.save()
                    request.session['cookie'] = user.cookie
                    return JsonResponse({'success': True})

                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Неправильный Логин или Пароль.'
                    })
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Неправильный Логин или Пароль.'
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
        user = check_user(request)
        if str(user) in ('Учитель', 'Ученик'):
            context = {
                'user': user,
                'requests': Student.objects.filter(accept=False, user_class=user.user_class)
            }

            return render(request, 'digitalDR/requestsStudents.html', context=context)

        else:
            return user

    def post(self, request):
        res = request.POST

        user_id = int(res['id'])
        act = res['type']

        if act == 'accept':
            user = Student.objects.get(id=user_id)
            user.accept = True
            user.save()
            return JsonResponse({
                'success': True
            })
        else:
            user = Student.objects.get(id=user_id)
            user.user_class = None
            user.save()
            return JsonResponse({
                'success': True
            })


class Settings(View):
    def get(self, request):
        user = check_user(request)
        if str(user) in ('Учитель', 'Ученик'):
            context = {
                'user': user,
                'dinner': user.dinner_days,
                'lunch': user.lunch_days
            }
            if user.card_num != '':
                context['schoolId'] = user.card_num.split('-')[0]
                context['cardId'] = user.card_num.split('-')[1]

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

        return JsonResponse({'success': True})


class Balance(View):
    def get(self, request):
        user = check_user(request)
        if str(user) in ('Учитель', 'Ученик'):
            if user.card_num:
                res = check_balance(user.card_num)
                if res == 'Счёт не найден.':
                    res = 'Вы указали неправильный счёт. Пожалуйста, проверьте свой баланс в настройках.'
            else:
                res = 'Вы не указали свой счёт в настройках.'

            context = {
                'user': user,
                'balance': res
            }

            return render(request, 'digitalDR/balance.html', context=context)

        else:
            return user


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
