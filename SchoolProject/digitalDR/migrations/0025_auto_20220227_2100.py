# Generated by Django 3.1.7 on 2022-02-27 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('digitalDR', '0024_auto_20220227_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cookie',
            field=models.CharField(default='gki7XAUXuPpjRqmlfdFa3HIDh41mrCc1WIQH7MNK', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_code',
            field=models.CharField(default='Jxam11xMcqOJDjF6', max_length=16, unique=True, verbose_name='Код'),
        ),
        migrations.CreateModel(
            name='UserMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dinner_days', models.JSONField(default={'Вт': False, 'Пн': False, 'Пт': False, 'Ср': False, 'Чт': False})),
                ('lunch_days', models.JSONField(default={'Вт': False, 'Пн': False, 'Пт': False, 'Ср': False, 'Чт': False})),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
