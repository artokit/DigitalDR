from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import *
import uuid
import hashlib


def f(request):
    return HttpResponse(request.session['cookie'])


class Index(View):
    def get(self, request):
        select = Class.objects.all()
        return render(request, 'digitalDR/about.html', {'select': select})


class MenuView(View):
    def get(self, request):
        try:
            cookie = request.session['cookie']
            user = CustomUser.objects.get(cookie=cookie)
            context = {
                'user': user,
            }

            return render(request, 'digitalDR/menu.html', context=context)

        except KeyError:
            return render(request, 'digitalDR/ERROR/KeyError.html')

        except CustomUser.DoesNotExist:
            return render(request, 'digitalDR/ERROR/KeyError.html')


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

        if CustomUser.objects.filter(username=res['username'][0]):
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

        if CustomUser.objects.filter(email=res['email'][0]):
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

        user = CustomUser(**{
            'name': res['first_name'][0],
            'last_name': res['last_name'][0],
            'email': res['email'][0],
            'username': res['username'][0],
            'password': Password(res['password'][0]).hash_password(),
            'user_class': Class.objects.get(name_class=res['user_class'][0])
        })

        user.save()

        request.session['cookie'] = user.cookie
        return JsonResponse({'success': True})


class Login(View):
    def post(self, request):
        res = request.POST
        if res['mode'] == 'teacher':
            code = res['code']
            try:
                user = CustomUser.objects.get(teacher_code=code)
                user.cookie = generate_s(40)
                user.save()
                request.session['cookie'] = user.cookie
                return JsonResponse({
                    'success': True,
                    'message': ''
                })
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Данного кода не существует.'
                })


class Main(View):
    def get(self, request):
        try:
            cookie = request.session['cookie']
            user = CustomUser.objects.get(cookie=cookie)
            context = {
                'user': user,
            }

            return render(request, 'digitalDR/main.html', context=context)

        except KeyError:
            return render(request, 'digitalDR/ERROR/KeyError.html')

        except CustomUser.DoesNotExist:
            return render(request, 'digitalDR/ERROR/KeyError.html')


class Settings(View):
    def get(self, request):
        try:
            cookie = request.session['cookie']
            user = CustomUser.objects.get(cookie=cookie)
            context = {
                'user': user,
            }
            return render(request, 'digitalDR/settings.html', context=context)

        except KeyError:
            return render(request, 'digitalDR/ERROR/KeyError.html')

        except CustomUser.DoesNotExist:
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

