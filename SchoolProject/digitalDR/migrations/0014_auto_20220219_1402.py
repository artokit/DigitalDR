# Generated by Django 3.1.7 on 2022-02-19 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0013_auto_20220219_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='is_teacher',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cookie',
            field=models.CharField(default='DcE0Ttwx2tnexwCL9psTJRKQhnWHLgrrMIQAnqJp', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_code',
            field=models.CharField(default='D8GKSCRwDCPxMam0', max_length=16, unique=True, verbose_name='Код'),
        ),
    ]
