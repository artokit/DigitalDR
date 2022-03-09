from django.db import models
from django.contrib.auth.models import User


class Menu(models.Model):
    name = models.CharField(max_length=150)
    cost = models.IntegerField()

    def __str__(self):
        return self.name


class Class(models.Model):
    name_class = models.CharField(max_length=10)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name_class


class RequestUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


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
