from django.shortcuts import render
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.core import serializers
from .models import *


def index(request):
    form = UserRegisterForm()
    return render(request, 'digitalDR/about.html', {'form': form})


def menu(request):
    return render(request, 'digitalDR/menu.html')


def get_menu(request):
    menu = Menu.objects.all()
    return HttpResponse(serializers.serialize('json', menu), content_type='application/json')
