# Generated by Django 3.1.7 on 2022-02-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0018_auto_20220219_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='dinner_days',
        ),
        migrations.RemoveField(
            model_name='student',
            name='lunch_days',
        ),
        migrations.AddField(
            model_name='customuser',
            name='dinner_days',
            field=models.JSONField(default={'Вторник': False, 'Понедельник': False, 'Пятница': False, 'Среда': False, 'Четверг': False}),
        ),
        migrations.AddField(
            model_name='customuser',
            name='lunch_days',
            field=models.JSONField(default={'Вторник': False, 'Понедельник': False, 'Пятница': False, 'Среда': False, 'Четверг': False}),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cookie',
            field=models.CharField(default='mowC4QFlNChVbDJcg8qg7EZ6LD24xqcsnOECqnES', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_code',
            field=models.CharField(default='Avu0FNSS7uIEuCqC', max_length=16, unique=True, verbose_name='Код'),
        ),
    ]
