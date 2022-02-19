# Generated by Django 3.1.7 on 2022-02-18 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0010_auto_20220215_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='card_num',
            field=models.CharField(blank=True, max_length=30, verbose_name='Номер Карты'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cookie',
            field=models.CharField(default='TyAsOIupXi3Ikros1SgF2MDwEobJRSYuJDN9t9hO', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='teacher_code',
            field=models.CharField(default='fpiQgHjguvxVHGH4', max_length=16, unique=True, verbose_name='Код'),
        ),
    ]
