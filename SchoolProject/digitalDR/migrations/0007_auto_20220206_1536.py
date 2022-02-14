# Generated by Django 3.1.7 on 2022-02-06 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0006_auto_20220206_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookie',
            name='cookie',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.TextField(unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='Учитель'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='teacher_code',
            field=models.CharField(default='RtAE8SDiwYG1TxEu', max_length=16, unique=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='digitalDR.class', verbose_name='Класс'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='Логин'),
        ),
    ]
