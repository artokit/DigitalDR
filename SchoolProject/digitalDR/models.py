from django.db import models
import random
from django.contrib.auth.models import User


def generate_s(length):
    s = ''
    letters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    for i in range(length):
        s += random.choice(list(letters))
    return s


class Menu(models.Model):
    name = models.CharField(max_length=150)
    cost = models.IntegerField()

    def __str__(self):
        return self.name


class Class(models.Model):
    name_class = models.CharField(max_length=10)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name_class


class CustomUser(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=False, verbose_name="Фамилия")
    email = models.TextField(blank=False, unique=True, verbose_name="Email")
    username = models.CharField(max_length=150, unique=True, blank=False, verbose_name="Логин")
    password = models.CharField(max_length=150, blank=False, verbose_name="Пароль")
    user_class = models.ForeignKey(Class, on_delete=models.CASCADE, default=1, blank=True, verbose_name='Класс', null=True)
    cookie = models.CharField(max_length=40, unique=True, default=generate_s(40))
    card_num = models.CharField(max_length=30, blank=True, verbose_name='Номер Карты')
    default_days = {
        'Пн': False,
        'Вт': False,
        'Ср': False,
        'Чт': False,
        'Пт': False,
    }
    dinner_days = models.JSONField(default=default_days)
    lunch_days = models.JSONField(default=default_days)

    def __str__(self):
        return self.username


class UserMenu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_days = {
        'Пн': False,
        'Вт': False,
        'Ср': False,
        'Чт': False,
        'Пт': False,
    }
    dinner_days = models.JSONField(default=default_days)
    lunch_days = models.JSONField(default=default_days)


class Teacher(CustomUser):
    teacher_code = models.CharField(
        max_length=16,
        default=generate_s(16),
        unique=True,
        verbose_name='Код'
    )

    def __str__(self):
        return 'Учитель'


class Student(CustomUser):
    accept = models.BooleanField(default=False)

    def __str__(self):
        return 'Ученик'