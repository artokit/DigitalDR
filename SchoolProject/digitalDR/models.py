from django.db import models
import random


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

    def __str__(self):
        return self.name_class


class CustomUser(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=False, verbose_name="Фамилия")
    email = models.TextField(blank=False, unique=True, verbose_name="Email")
    username = models.CharField(max_length=150, unique=True, blank=False, verbose_name="Логин")
    password = models.CharField(max_length=150, blank=False, verbose_name="Пароль")
    user_class = models.ForeignKey(Class, on_delete=models.CASCADE, default=1, blank=False, verbose_name='Класс')
    is_teacher = models.BooleanField(default=False, verbose_name="Учитель")
    teacher_code = models.CharField(
        max_length=16,
        default=generate_s(16),
        unique=True,
        verbose_name='Код'
    )
    cookie = models.CharField(max_length=40, unique=True, default=generate_s(40))

    def __str__(self):
        return self.username
