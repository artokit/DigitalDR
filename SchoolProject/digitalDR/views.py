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
import datetime
from pysimplesoap.client import SoapClient

WSDL_URL = 'http://94.181.180.222:7581/DemoSchBuff/ws/SchBuffPayments?wsdl'
client = SoapClient(wsdl=WSDL_URL, ns="web", trace=True)


def check_balance(card):
    hot_meal = client.balanseInfo(cardID=card, password=card)['return']
    if hot_meal['code'] == '2':
        return {'success': False, 'text': 'Данная карта не существует'}

    data = {
        'success': True,
        'hot_meal_money': hot_meal['otherData']['paymentData']['descr']
    }

    return data


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
    model = UserInformation

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['requests'] = []
        teacher_class = Class.objects.get(pk=UserInformation.objects.get(user=self.request.user).user_class.pk)

        for user in UserInformation.objects.filter(user_class=teacher_class, is_accept=False):
            context['requests'].append(user.user)

        return {**context, **self.get_user_context(user=self.request.user)}


class RequestsStudentsPost(DataMixin, FormView):
    def post(self, request, *args, **kwargs):
        res = self.request.POST
        user = User.objects.get(pk=res['id'])
        user_info = UserInformation.objects.get(user=user)
        if res['type'] == 'accept':
            user_info.is_accept = True

        else:
            user_info.user_class = Class.objects.get(name_class='kicked')

        user_info.save()
        return JsonResponse({'success': True})


class Settings(DataMixin, TemplateView):
    template_name = 'digitalDR/settings.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return {**context, **self.get_user_context(user=self.request.user)}

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)


class Login(LoginView):
    template_name = 'digitalDR/login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        if str(self.request.user) != 'AnonymousUser':
            return redirect('menu')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('menu')


class Register(DataMixin, CreateView):
    model = User
    template_name = 'digitalDR/register.html'
    form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        if str(self.request.user) != 'AnonymousUser':
            return redirect('menu')
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        user.groups.add(Group.objects.get(name='Ученик'))
        user.save()
        u = UserInformation(user=user)
        u.save()
        return redirect('ChangeUserInformation')


class Orders(DataMixin, ListView):
    template_name = 'digitalDR/orders.html'
    model = User
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        teacher_class = Class.objects.get(pk=UserInformation.objects.get(user=self.request.user).user_class.pk)
        context['lunch_count'] = 0
        context['dinner_count'] = 0
        if datetime.datetime.today().weekday() < 5:
            for user in UserInformation.objects.filter(user_class=teacher_class, is_accept=True):
                today = datetime.datetime.today().weekday()

                if list(user.dinner_days.values())[today]:
                    context['dinner_count'] += 1

                if list(user.lunch_days.values())[today]:
                    context['lunch_count'] += 1

        return {**context, **self.get_user_context(user=self.request.user)}

    def get_queryset(self):
        teacher_class = Class.objects.get(pk=UserInformation.objects.get(user=self.request.user).user_class.pk)
        return UserInformation.objects.filter(user_class=teacher_class, is_accept=True)

    def post(self, request):
        # TODO: Доделать защиту.
        res = request.POST

        if res['act'] == 'kick':
            user_kick = UserInformation.objects.get(user=User.objects.get(pk=res['user_id']))
            user_kick.is_accept = False
            user_kick.user_class = Class.objects.get(pk=4)
            user_kick.save()
            return JsonResponse({'success': True})

        if res['act'] == 'info':
            user = UserInformation.objects.get(user=User.objects.get(pk=res['user_id']))

            balance_card = '0'

            if user.card_num:
                balance_card = check_balance(user.card_num)['hot_meal_money']

            return JsonResponse({
                'success': True,
                'card_num': user.card_num if user.card_num else 'Пользователь не указал карту',
                'lunch': user.lunch_days,
                'dinner': user.dinner_days,
                'balance_card': balance_card
            })


# Todo: не работает.
class ChangePassword(DataMixin, FormView):
    template_name = 'digitalDR/changePassword.html'

    def get_form(self, form_class=None):
        return PasswordChangeForm(self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return {**context, **self.get_user_context(user=self.request.user)}

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        return super().post(self.request)

    def form_valid(self, form):
        form.save()
        return redirect('settings')

    def form_invalid(self, form):
        print(form.error_messages)


class ChangeFoodMenu(DataMixin, UpdateView):
    template_name = 'digitalDR/changeFoodMenu.html'
    model = UserInformation
    context_object_name = 'food'
    fields = '__all__'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return {**context, **self.get_user_context(user=self.request.user)}

    def get_object(self, queryset=None):
        return UserInformation.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        res = json.loads(self.request.POST['data'])
        user_menu = UserInformation.objects.get(user=self.request.user)
        user_menu.dinner_days = res['dinner']
        user_menu.lunch_days = res['lunch']
        user_menu.save()
        return JsonResponse({'success': True})


def user_logout(request):
    logout(request)
    return redirect('login')


class ChangeUserInformationView(DataMixin, UpdateView):
    model = User
    template_name = 'digitalDR/changeInformation.html'
    fields = ('first_name', 'last_name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['classes'] = Class.objects.all()
        context['user_info'] = UserInformation.objects.get(user=self.request.user)
        return {**context, **self.get_user_context(user=self.request.user)}

    def get_object(self, queryset=None):
        return UserInformation.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        res = self.request.POST
        user = self.request.user
        user_info = UserInformation.objects.get(user=user)

        if res['first_name']:
            user.first_name = res['first_name']

        if res['last_name']:
            user.last_name = res['last_name']

        user_info.user_class = Class.objects.get(name_class=res['user_class'])

        if not user.groups.filter(id=5):
            user_info.is_accept = False

        user_info.save()
        user.save()

        return JsonResponse({'success': True})


class BalanceView(DataMixin, TemplateView):
    template_name = 'digitalDR/balance.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['classes'] = Class.objects.all()
        context['user_info'] = UserInformation.objects.get(user=self.request.user)
        if context['user_info'].card_num:
            context['user_balance'] = check_balance(context['user_info'].card_num)['hot_meal_money']
        return {**context, **self.get_user_context(user=self.request.user)}

    def post(self, request):
        res = self.request.POST
        user = request.user
        user_info = UserInformation.objects.get(user=user)

        info = check_balance(res['card_num'])

        if not info['success']:
            return JsonResponse({'success': False, 'text': info['text']})

        del info['success']

        user_info.card_num = res['card_num']
        user_info.save()

        return JsonResponse({'success': True, 'result': info})

