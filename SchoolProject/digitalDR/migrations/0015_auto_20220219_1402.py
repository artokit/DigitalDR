# Generated by Django 3.1.7 on 2022-02-19 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0014_auto_20220219_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='is_teacher',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cookie',
            field=models.CharField(default='4hkKJg4T83qk3yZzNVZJinwRKFEDyQpfH0DA6N1m', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_code',
            field=models.CharField(default='V3lzeuYB9uI2L8Un', max_length=16, unique=True, verbose_name='Код'),
        ),
    ]
