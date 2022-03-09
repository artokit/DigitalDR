from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, FormView, TemplateView, CreateView, UpdateView
from .utils import DataMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group
from django.core import serializers
from .models import *
import json
import requests
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


class RequestsStudents(DataMixin, ListView):
    template_name = 'digitalDR/requestsStudents.html'
    model = RequestUser

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['requests'] = []
        teacher_class = Class.objects.get(user=self.request.user)

        for user in teacher_class.user.all():
            if RequestUser.objects.filter(user=user):
                context['requests'].append(user)

        return {**context, **self.get_user_context(user=self.request.user)}


class RequestsStudentsPost(DataMixin, FormView):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.POST['id'])
        r = RequestUser.objects.get(user=user)
        r.delete()
        return JsonResponse({'success': True})


class Settings(DataMixin, TemplateView):
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

    def get_success_url(self):
        return reverse('menu')


class Register(DataMixin, CreateView):
    model = User
    template_name = 'digitalDR/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        req = RequestUser()
        req.user = user
        req.save()

        user.groups.add(Group.objects.get(name='Ученик'))

        user.save()
        return redirect('menu')


class Orders(DataMixin, ListView):
    template_name = 'digitalDR/orders.html'
    model = User
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        teacher_class = Class.objects.get(user=self.request.user)
        context['lunch_count'] = 0
        context['dinner_count'] = 0
        if datetime.datetime.today().weekday() < 5:
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
        return {user: UserMenu.objects.get(user=user) for user in teacher_class.user.all() if not RequestUser.objects.filter(user=user)}


# Todo: не работает.
class ChangePassword(DataMixin, FormView):
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'digitalDR/changePassword.html'

    def get_form(self, form_class=None):
        return PasswordChangeForm(self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return {**context, **self.get_user_context(user=self.request.user)}


class ChangeFoodMenu(DataMixin, UpdateView):
    template_name = 'digitalDR/changeFoodMenu.html'
    model = UserMenu
    context_object_name = 'food'
    fields = '__all__'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return {**context, **self.get_user_context(user=self.request.user)}

    def get_object(self, queryset=None):
        try:
            return UserMenu.objects.get(user=self.request.user)

        except UserMenu.DoesNotExist:
            user_menu = UserMenu()
            user_menu.user = self.request.user
            user_menu.lunch_days = UserMenu.default_days
            user_menu.dinner_days = UserMenu.default_days
            user_menu.save()
            return user_menu

    def post(self, request, *args, **kwargs):
        res = json.loads(self.request.POST['data'])
        user_menu = UserMenu.objects.get(user=self.request.user)
        user_menu.dinner_days = res['dinner']
        user_menu.lunch_days = res['lunch']
        user_menu.save()
        return JsonResponse({'success': True})


def user_logout(request):
    logout(request)
    return redirect('login')
