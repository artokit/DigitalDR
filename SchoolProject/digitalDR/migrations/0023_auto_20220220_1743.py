# Generated by Django 3.1.7 on 2022-02-20 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0022_auto_20220220_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cookie',
            field=models.CharField(default='8lFKNMsGvDYnt8oLywhGuVTu3urvtYk0ET0bsN5q', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_class',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalDR.class', verbose_name='Класс'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_code',
            field=models.CharField(default='jKJQirTHzuVafgkY', max_length=16, unique=True, verbose_name='Код'),
        ),
    ]
