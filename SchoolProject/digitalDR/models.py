from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=150)
    cost = models.IntegerField()

    def __str__(self):
        return self.name
